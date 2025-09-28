#!/usr/bin/env python3
"""
Railway Deployment Script for LangGraph AI Agent
Optimized for Railway's environment and requirements
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Setup Python path and environment for Railway"""
    project_root = Path(__file__).parent
    
    # Add paths to Python path
    sys.path.insert(0, str(project_root / "src"))
    sys.path.insert(0, str(project_root / "backend"))
    
    # Set environment variables for Railway
    os.environ["PYTHONPATH"] = f"{project_root}/src:{project_root}/backend"
    
    print("✅ Environment configured for Railway deployment")

def check_dependencies():
    """Check if all required dependencies are installed"""
    requirements_file = Path("backend/requirements.txt")
    
    if not requirements_file.exists():
        print("❌ Backend requirements.txt not found")
        return False
    
    try:
        # Check if FastAPI is available
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__} available")
        
        # Check if our backend main module can be imported
        from backend.main import app
        print("✅ Backend main module imports successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Run: pip install -r backend/requirements.txt")
        return False

def start_server():
    """Start the FastAPI server for Railway"""
    port = os.getenv("PORT", "8000")
    
    print(f"🚀 Starting LangGraph AI Agent on port {port}")
    print(f"🌍 Server will be available at: http://0.0.0.0:{port}")
    
    # Start uvicorn server
    cmd = [
        "uvicorn", 
        "backend.main:app", 
        "--host", "0.0.0.0", 
        "--port", port,
        "--workers", "1"
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    print("🚂 LangGraph AI Agent - Railway Deployment")
    print("=" * 50)
    
    setup_environment()
    
    if check_dependencies():
        start_server()
    else:
        print("❌ Dependency check failed. Cannot start server.")
        sys.exit(1)