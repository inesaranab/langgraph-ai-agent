"""
FastAPI Backend for LangGraph AI Agent
Provides REST API endpoints for the React frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, AsyncGenerator
import uuid
from datetime import datetime
import os
import json
import asyncio
from dotenv import load_dotenv

# Import your existing agent
import sys
import os

# Add both the parent directory and src directory to Python path
parent_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, parent_dir)
sys.path.insert(0, src_dir)

from src.agents.langgraph_agent import LangGraphAgent
from src.utils.config import AppConfig

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="LangGraph AI Agent API",
    description="REST API for LangGraph AI Agent",
    version="1.0.0"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
config = AppConfig()
agent = None

# Request/Response models
class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    conversation_history: Optional[List[ChatMessage]] = []
    openai_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    metadata: Dict[str, Any]
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    agent_ready: bool
    api_keys_configured: bool

# In-memory session storage (use Redis in production)
sessions = {}

def get_agent_with_keys(openai_key: Optional[str] = None, tavily_key: Optional[str] = None):
    """Get agent instance with provided API keys"""
    try:
        if openai_key and tavily_key:
            return LangGraphAgent(config, openai_key, tavily_key)
        elif agent is not None:
            return agent
        else:
            raise ValueError("No API keys provided and no default agent available")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to initialize agent: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup"""
    global agent
    try:
        # Initialize with environment variables as fallback
        openai_key = os.getenv("OPENAI_API_KEY")
        tavily_key = os.getenv("TAVILY_API_KEY")
        if openai_key and tavily_key:
            agent = LangGraphAgent(config, openai_key, tavily_key)
            print("Agent initialized successfully with environment keys")
        else:
            print("No API keys in environment - will require user-provided keys")
    except Exception as e:
        print(f"Failed to initialize agent: {e}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        agent_ready=agent is not None,
        api_keys_configured=bool(os.getenv("OPENAI_API_KEY") and os.getenv("TAVILY_API_KEY"))
    )

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint"""
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # Store conversation history
    if session_id not in sessions:
        sessions[session_id] = []
    
    # Add user message to history
    user_message = ChatMessage(
        role="user",
        content=request.message,
        timestamp=datetime.now()
    )
    sessions[session_id].append(user_message)
    
    async def generate_response():
        try:
            # Send initial metadata
            yield f"data: {json.dumps({'type': 'start', 'session_id': session_id})}\n\n"
            
            # Get agent with provided API keys
            current_agent = get_agent_with_keys(request.openai_api_key, request.tavily_api_key)
            
            # Process query with agent
            response_data = current_agent.process_query(request.message, session_id)
            
            # Stream the response in chunks
            full_response = response_data.get("response", "No response generated")
            metadata = response_data.get("metadata", {})
            
            # Simulate streaming by breaking response into words
            words = full_response.split(' ')
            current_text = ""
            
            for i, word in enumerate(words):
                current_text += word + " "
                chunk_data = {
                    'type': 'chunk',
                    'content': word + " ",
                    'full_content': current_text.strip(),
                }
                yield f"data: {json.dumps(chunk_data)}\n\n"
                await asyncio.sleep(0.05)  # Small delay for streaming effect
            
            # Send final metadata
            final_data = {
                'type': 'done',
                'metadata': metadata,
                'timestamp': datetime.now().isoformat()
            }
            yield f"data: {json.dumps(final_data)}\n\n"
            
            # Add assistant message to history
            assistant_message = ChatMessage(
                role="assistant",
                content=full_response,
                timestamp=datetime.now(),
                metadata=metadata
            )
            sessions[session_id].append(assistant_message)
            
        except Exception as e:
            error_data = {
                'type': 'error',
                'error': str(e)
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        }
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint (non-streaming fallback)"""
    # Get agent with provided API keys
    current_agent = get_agent_with_keys(request.openai_api_key, request.tavily_api_key)
    
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # Store conversation history
    if session_id not in sessions:
        sessions[session_id] = []
    
    # Add user message to history
    user_message = ChatMessage(
        role="user",
        content=request.message,
        timestamp=datetime.now()
    )
    sessions[session_id].append(user_message)
    
    try:
        # Process query with agent
        response_data = current_agent.process_query(request.message, session_id)
        
        # Create response
        response = ChatResponse(
            response=response_data.get("response", "No response generated"),
            session_id=session_id,
            metadata=response_data.get("metadata", {}),
            timestamp=datetime.now()
        )
        
        # Add assistant message to history
        assistant_message = ChatMessage(
            role="assistant",
            content=response.response,
            timestamp=response.timestamp,
            metadata=response.metadata
        )
        sessions[session_id].append(assistant_message)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/chat/{session_id}/history", response_model=List[ChatMessage])
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    if session_id not in sessions:
        return []
    return sessions[session_id]

@app.delete("/chat/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear chat history for a session"""
    if session_id in sessions:
        del sessions[session_id]
    return {"message": "Chat history cleared"}

@app.get("/sessions")
async def get_sessions():
    """Get all active sessions"""
    return {
        "sessions": list(sessions.keys()),
        "total_sessions": len(sessions)
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)