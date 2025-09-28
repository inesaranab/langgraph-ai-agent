"""
Full-Stack FastAPI + React for Railway
Serves both API and frontend from single service
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
import os
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(
    title="LangGraph AI Agent - Full Stack",
    description="Full-stack app with React frontend + FastAPI backend",
    version="1.0.0"
)

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
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

# API Routes
@app.get("/health", response_model=HealthResponse)
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check - works on both /health and /api/health"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        message="🚂 Railway Full-Stack deployment! Frontend + Backend working together."
    )

@app.post("/chat", response_model=ChatResponse)
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint - works on both /chat and /api/chat"""
    
    session_id = request.session_id or str(uuid.uuid4())
    
    # Simple echo response for now
    response_text = f"""🤖 **Full-Stack Railway Response**

**Your message:** {request.message}

✅ **Status:** Frontend + Backend working together!  
🚂 **Platform:** Railway  
🎨 **Frontend:** React + Next.js  
⚙️ **Backend:** FastAPI  
📡 **API Keys:** {'✅ Received' if request.openai_api_key else '❌ Not provided'}

🔗 **Architecture:** Single Railway service serving both frontend and backend!"""
    
    response = ChatResponse(
        response=response_text,
        session_id=session_id,
        metadata={
            "mode": "fullstack_railway",
            "frontend": "react_nextjs",
            "backend": "fastapi",
            "deployment": "railway_single_service",
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

@app.get("/sessions")
@app.get("/api/sessions")
async def get_sessions():
    """Get sessions - works on both endpoints"""
    return {
        "sessions": list(sessions.keys()),
        "total_sessions": len(sessions),
        "deployment": "railway_fullstack",
        "architecture": "frontend_and_backend_combined"
    }

@app.get("/chat/{session_id}/history")
@app.get("/api/chat/{session_id}/history")
async def get_chat_history(session_id: str):
    """Get chat history"""
    return sessions.get(session_id, [])

@app.delete("/chat/{session_id}")
@app.delete("/api/chat/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear chat history"""
    if session_id in sessions:
        del sessions[session_id]
    return {"message": "Chat history cleared", "session_id": session_id}

# Frontend Static Files (if built frontend exists)
frontend_dir = Path(__file__).parent.parent / "frontend" / ".next" / "standalone"
if frontend_dir.exists():
    # Mount the built frontend
    app.mount("/static", StaticFiles(directory=str(frontend_dir / ".next" / "static")), name="static")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve React frontend for all non-API routes"""
        
        # Don't serve frontend for API routes
        if full_path.startswith("api/") or full_path in ["health", "chat", "sessions", "docs", "redoc", "openapi.json"]:
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # Serve index.html for all frontend routes
        index_file = frontend_dir / "server.js"  # Next.js standalone
        if index_file.exists():
            return FileResponse(str(index_file))
        
        # Fallback
        raise HTTPException(status_code=404, detail="Frontend not built")

# Startup message
@app.on_event("startup")
async def startup_event():
    print("🚀 LangGraph AI Agent - Full Stack Railway Deployment")
    print("🎨 Frontend: React + Next.js")
    print("⚙️ Backend: FastAPI")
    print("🚂 Platform: Railway")
    print("✅ Single service deployment ready!")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)