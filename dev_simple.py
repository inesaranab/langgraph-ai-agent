#!/usr/bin/env python3
"""
Simple Development Server for LangGraph AI Agent
Local development only - no complex configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Setup basic environment for development"""
    project_root = Path(__file__).parent
    
    # Add paths
    sys.path.insert(0, str(project_root / "src"))
    sys.path.insert(0, str(project_root / "backend"))
    
    # Set basic environment
    os.environ["PYTHONPATH"] = f"{project_root}/src:{project_root}/backend"
    
    print("✅ Development environment ready")

def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️ .env file not found")
        print("💡 Copy .env.example to .env and add your API keys")
        return False
    print("✅ .env file found")
    return True

def start_backend():
    """Start the FastAPI backend for development"""
    print("🚀 Starting LangGraph AI Agent Backend...")
    print("🌍 Backend will be available at: http://localhost:8000")
    print("📖 API docs at: http://localhost:8000/docs")
    
    # Start uvicorn
    cmd = [
        "uvicorn", 
        "backend.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--reload"  # Auto-reload on changes for development
    ]
    
    subprocess.run(cmd)

def start_frontend():
    """Start the React frontend for development"""
    print("🎨 Starting React Frontend...")
    print("🌍 Frontend will be available at: http://localhost:3000")
    
    os.chdir("frontend")
    subprocess.run(["npm", "run", "dev"])

if __name__ == "__main__":
    print("🔧 LangGraph AI Agent - Development Server")
    print("=" * 50)
    
    setup_environment()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "frontend":
            start_frontend()
        elif sys.argv[1] == "backend":
            start_backend()
        else:
            print("Usage: python dev_simple.py [frontend|backend]")
    else:
        # Default: start backend
        check_env_file()
        start_backend()