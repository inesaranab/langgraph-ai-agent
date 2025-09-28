from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any
import os
import sys
import json
import asyncio
from fastapi.responses import StreamingResponse

# Add project paths to Python path for Vercel
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))
sys.path.insert(0, os.path.join(project_root, 'backend'))

# Create FastAPI app for Vercel serverless
app = FastAPI(title="LangGraph AI Agent API")

# CORS configuration for Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import LangGraph agent
try:
    sys.path.append('/var/task/src')
    sys.path.append('/var/task/backend')
    from agents.langgraph_agent import LangGraphAgent
    from utils.config import AppConfig
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"Agent import failed: {e}")
    AGENT_AVAILABLE = False

# Request/Response models
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    agent_ready: bool
    api_keys_configured: bool
    platform: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    conversation_history: Optional[List[Dict]] = []
    openai_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    metadata: Dict[str, Any]
    timestamp: datetime

# In-memory session storage (Vercel limitations)
sessions = {}

# Health endpoint
@app.get("/health", response_model=HealthResponse)
@app.get("/", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        agent_ready=AGENT_AVAILABLE,
        api_keys_configured=bool(os.getenv("OPENAI_API_KEY") and os.getenv("TAVILY_API_KEY")),
        platform="vercel-serverless"
    )

# Main chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not AGENT_AVAILABLE:
        # Fallback response when agent is not available
        return ChatResponse(
            response=f"Echo: {request.message} (Agent not available in serverless mode)",
            session_id=request.session_id or "fallback-session",
            metadata={
                "tools_used": ["fallback"],
                "processing_time": 0.1,
                "platform": "vercel-serverless"
            },
            timestamp=datetime.now()
        )
    
    try:
        # Initialize agent with user-provided API keys
        if not request.openai_api_key or not request.tavily_api_key:
            raise HTTPException(status_code=400, detail="OpenAI and Tavily API keys required")
        
        config = AppConfig()
        agent = LangGraphAgent(config, request.openai_api_key, request.tavily_api_key)
        
        # Process the query
        session_id = request.session_id or f"session-{datetime.now().timestamp()}"
        response_data = agent.process_query(request.message, session_id)
        
        return ChatResponse(
            response=response_data.get("response", "No response generated"),
            session_id=session_id,
            metadata=response_data.get("metadata", {}),
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Streaming chat endpoint
@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def generate_response():
        try:
            if not request.openai_api_key or not request.tavily_api_key:
                yield f"data: {json.dumps({'type': 'error', 'error': 'API keys required'})}\n\n"
                return
            
            # Send start message
            session_id = request.session_id or f"session-{datetime.now().timestamp()}"
            yield f"data: {json.dumps({'type': 'start', 'session_id': session_id})}\n\n"
            
            if AGENT_AVAILABLE:
                # Initialize and use real agent
                config = AppConfig()
                agent = LangGraphAgent(config, request.openai_api_key, request.tavily_api_key)
                response_data = agent.process_query(request.message, session_id)
                
                full_response = response_data.get("response", "No response generated")
                metadata = response_data.get("metadata", {})
            else:
                # Fallback response
                full_response = f"Echo: {request.message} (Serverless fallback mode)"
                metadata = {"platform": "vercel-serverless", "mode": "fallback"}
            
            # Stream the response word by word
            words = full_response.split(' ')
            current_text = ""
            
            for word in words:
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
            
        except Exception as e:
            error_data = {'type': 'error', 'error': str(e)}
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

# Session management
@app.get("/sessions")
async def get_sessions():
    return {
        "sessions": list(sessions.keys()),
        "total_sessions": len(sessions),
        "platform": "vercel-serverless"
    }

@app.get("/chat/{session_id}/history")
async def get_chat_history(session_id: str):
    return sessions.get(session_id, [])

@app.delete("/chat/{session_id}")
async def clear_chat_history(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
    return {"message": "Chat history cleared"}

# Vercel handler
handler = app