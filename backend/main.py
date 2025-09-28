"""
Simple FastAPI Backend for LangGraph AI Agent
Streamlined for Railway deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime
import os
import json
import asyncio
import sys

# Add paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Initialize FastAPI app
app = FastAPI(
    title="LangGraph AI Agent API",
    description="Simple REST API for LangGraph AI Agent",
    version="1.0.0"
)

# Simple CORS - allow all for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to import LangGraph agent with fallback
try:
    from agents.langgraph_agent import LangGraphAgent
    from utils.config import AppConfig
    AGENT_AVAILABLE = True
    print("✅ LangGraph agent imported successfully")
except ImportError as e:
    print(f"⚠️ LangGraph agent import failed: {e}")
    AGENT_AVAILABLE = False

# Simple data models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
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
    agent_available: bool

# In-memory sessions
sessions = {}

@app.get("/health", response_model=HealthResponse)
@app.get("/", response_model=HealthResponse) 
async def health_check():
    """Simple health check"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        agent_available=AGENT_AVAILABLE
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Simple chat endpoint"""
    
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    if not AGENT_AVAILABLE:
        # Simple fallback when agent isn't available
        return ChatResponse(
            response=f"Echo: {request.message} (LangGraph agent not available - using fallback mode)",
            session_id=session_id,
            metadata={
                "mode": "fallback",
                "agent_available": False,
                "timestamp": datetime.now().isoformat()
            },
            timestamp=datetime.now()
        )
    
    try:
        # Initialize agent with provided API keys
        if not request.openai_api_key:
            raise HTTPException(status_code=400, detail="OpenAI API key required")
        
        # Import here to avoid issues if not available
        from utils.config import AppConfig
        from agents.langgraph_agent import LangGraphAgent
        
        config = AppConfig()
        agent = LangGraphAgent(config, request.openai_api_key, request.tavily_api_key)
        
        # Process the message (sync call, not async)
        result = agent.process_query(request.message)
        
        response = ChatResponse(
            response=result.get("response", "No response generated"),
            session_id=session_id,
            metadata=result.get("metadata", {}),
            timestamp=datetime.now()
        )
        
        # Store in session
        if session_id not in sessions:
            sessions[session_id] = []
        sessions[session_id].append({
            "message": request.message,
            "response": response.response,
            "timestamp": response.timestamp.isoformat()
        })
        
        return response
        
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.get("/chat/{session_id}/history")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    return sessions.get(session_id, [])

@app.delete("/chat/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear chat history for a session"""
    if session_id in sessions:
        del sessions[session_id]
    return {"message": "Chat history cleared", "session_id": session_id}

@app.get("/sessions")
async def get_sessions():
    """Get all active sessions"""
    return {
        "sessions": list(sessions.keys()),
        "total_sessions": len(sessions),
        "agent_available": AGENT_AVAILABLE
    }

# Simple startup message
@app.on_event("startup")
async def startup_event():
    print("🚀 LangGraph AI Agent API starting...")
    print(f"📊 Agent available: {AGENT_AVAILABLE}")
    print("✅ Server ready!")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)