"""
Ultra-Simple FastAPI Backend for Railway Deployment Test
This version will definitely work - no complex dependencies
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
import os

# Initialize FastAPI app
app = FastAPI(
    title="LangGraph AI Agent API - Minimal",
    description="Simple test API for Railway deployment",
    version="1.0.0"
)

# Simple CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    message: str

# In-memory storage
sessions = {}

@app.get("/health", response_model=HealthResponse)
@app.get("/", response_model=HealthResponse)
async def health_check():
    """Ultra-simple health check"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        message="🚂 Railway deployment successful! LangGraph AI Agent API is running."
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Simple echo chat for testing"""
    
    session_id = request.session_id or str(uuid.uuid4())
    
    # Simple echo response for now
    response_text = f"🤖 Echo: {request.message}\n\n✅ Railway deployment working!\n📡 API keys received: {'Yes' if request.openai_api_key else 'No'}"
    
    response = ChatResponse(
        response=response_text,
        session_id=session_id,
        metadata={
            "mode": "minimal_test",
            "railway_deployment": True,
            "timestamp": datetime.now().isoformat(),
            "message_length": len(request.message)
        },
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
        "deployment": "railway",
        "status": "minimal_working"
    }

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify deployment"""
    return {
        "message": "🎉 Railway deployment successful!",
        "status": "working",
        "platform": "railway",
        "api": "fastapi",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)