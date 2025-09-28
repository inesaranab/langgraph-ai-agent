"""Unified Full-Stack FastAPI entrypoint
Serves:
 - LangGraph agent API (full functionality)
 - Static exported Next.js frontend (if present)

Deployment modes:
 - LOCAL_DEV: run frontend separately (npm dev) and this API only
 - FULLSTACK: single container on Railway serving static export
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
import asyncio
import uuid
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# ---- LangGraph imports ----
import sys
parent_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, parent_dir)
sys.path.insert(0, src_dir)
from src.agents.langgraph_agent import LangGraphAgent
from src.utils.config import AppConfig

load_dotenv()

MODE = os.getenv("APP_MODE", "FULLSTACK").upper()

app = FastAPI(title="LangGraph AI Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    mode: str

sessions: Dict[str, List[ChatMessage]] = {}

config = AppConfig()
agent: Optional[LangGraphAgent] = None

def get_agent(openai_key: Optional[str], tavily_key: Optional[str]):
    if openai_key and tavily_key:
        return LangGraphAgent(config, openai_key, tavily_key)
    if agent:
        return agent
    raise HTTPException(status_code=400, detail="Agent not initialized and no API keys provided")

@app.on_event("startup")
async def startup():
    global agent
    env_oai = os.getenv("OPENAI_API_KEY")
    env_tav = os.getenv("TAVILY_API_KEY")
    if env_oai and env_tav:
        try:
            agent = LangGraphAgent(config, env_oai, env_tav)
            print("✅ LangGraph agent initialized with environment keys")
        except Exception as e:
            print(f"⚠️ Failed to init agent: {e}")
    else:
        print("ℹ️ No environment API keys; expecting runtime provided keys.")
    print(f"MODE={MODE}")

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        agent_ready=agent is not None,
        api_keys_configured=bool(os.getenv("OPENAI_API_KEY") and os.getenv("TAVILY_API_KEY")),
        mode=MODE
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    current_agent = get_agent(req.openai_api_key, req.tavily_api_key)
    session_id = req.session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = []
    # Add user message
    sessions[session_id].append(ChatMessage(role="user", content=req.message, timestamp=datetime.now()))
    data = current_agent.process_query(req.message, session_id)
    response_text = data.get("response", "No response generated")
    metadata = data.get("metadata", {})
    chat_resp = ChatResponse(response=response_text, session_id=session_id, metadata=metadata, timestamp=datetime.now())
    sessions[session_id].append(ChatMessage(role="assistant", content=response_text, timestamp=chat_resp.timestamp, metadata=metadata))
    return chat_resp

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    current_agent = get_agent(req.openai_api_key, req.tavily_api_key)
    session_id = req.session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = []
    sessions[session_id].append(ChatMessage(role="user", content=req.message, timestamp=datetime.now()))

    async def generate():
        try:
            yield f"data: {json.dumps({'type': 'start', 'session_id': session_id})}\n\n"
            data = current_agent.process_query(req.message, session_id)
            full = data.get('response', '')
            metadata = data.get('metadata', {})
            words = full.split(' ')
            current = ''
            for w in words:
                current += w + ' '
                yield f"data: {json.dumps({'type':'chunk','content':w+' ','full_content':current.strip()})}\n\n"
                await asyncio.sleep(0.02)
            yield f"data: {json.dumps({'type':'done','metadata':metadata})}\n\n"
            sessions[session_id].append(ChatMessage(role="assistant", content=full, timestamp=datetime.now(), metadata=metadata))
        except Exception as e:
            yield f"data: {json.dumps({'type':'error','error':str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/chat/{session_id}/history", response_model=List[ChatMessage])
async def history(session_id: str):
    return sessions.get(session_id, [])

@app.delete("/chat/{session_id}")
async def clear(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
    return {"message": "cleared", "session_id": session_id}

# ---- Static Frontend (only in FULLSTACK mode) ----
if MODE == "FULLSTACK":
    export_dir = Path(__file__).parent.parent / "frontend" / "dist"
    alt_dir = Path(__file__).parent.parent / "frontend" / "static"  # fallback name
    chosen = export_dir if export_dir.exists() else alt_dir
    if chosen.exists():
        app.mount("/", StaticFiles(directory=str(chosen), html=True), name="frontend")
        print(f"🗂  Serving static frontend from: {chosen}")
    else:
        print("⚠️ No static frontend directory found; API-only mode.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
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