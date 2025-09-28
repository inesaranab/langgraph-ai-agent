#!/usr/bin/env python3
"""
Development launcher for React + FastAPI version
Starts both backend and frontend servers
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def check_node():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Node.js found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("Node.js not found. Please install Node.js 18+ from https://nodejs.org")
    return False

def check_python_deps():
    """Check Python dependencies"""
    try:
        import fastapi
        import uvicorn
        print("Python backend dependencies installed")
        return True
    except ImportError:
        print("Python dependencies missing. Run: pip install -r backend/requirements.txt")
        return False

def install_frontend_deps():
    """Install frontend dependencies"""
    frontend_dir = Path("frontend")
    if not (frontend_dir / "node_modules").exists():
        print("Installing frontend dependencies...")
        result = subprocess.run(['npm', 'install'], cwd=frontend_dir)
        if result.returncode != 0:
            print("Failed to install frontend dependencies")
            return False
    
    print("Frontend dependencies ready")
    return True

def start_backend():
    """Start the FastAPI backend"""
    print("Starting FastAPI backend on http://localhost:8000")
    backend_dir = Path("backend")
    
    # Add src to Python path
    env = os.environ.copy()
    src_path = str(Path("src").absolute())
    if 'PYTHONPATH' in env:
        env['PYTHONPATH'] = f"{src_path}{os.pathsep}{env['PYTHONPATH']}"
    else:
        env['PYTHONPATH'] = src_path
    
    subprocess.run([
        sys.executable, "main.py"
    ], cwd=backend_dir, env=env)

def start_frontend():
    """Start the Next.js frontend"""
    print("Starting Next.js frontend on http://localhost:3000")
    frontend_dir = Path("frontend")
    subprocess.run(['npm', 'run', 'dev'], cwd=frontend_dir)

def main():
    """Main launcher function"""
    print("Starting LangGraph AI Agent - React + FastAPI Version")
    print("=" * 60)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check prerequisites
    if not check_node():
        sys.exit(1)
    
    if not check_python_deps():
        print("Installing backend dependencies...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'])
        if result.returncode != 0:
            print("Failed to install backend dependencies")
            sys.exit(1)
    
    if not install_frontend_deps():
        sys.exit(1)
    
    # Check environment file
    if not os.path.exists(".env"):
        print(".env file not found")
        print("Please copy .env.example to .env and add your API keys")
        sys.exit(1)
    
    print("\nAll checks passed!")
    print("\nStarting services...")
    print("Backend: http://localhost:8000")
    print("Frontend: http://localhost:3000")
    print("API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop both servers")
    print("=" * 60)
    
    try:
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # Give backend time to start
        time.sleep(3)
        
        # Start frontend (blocking)
        start_frontend()
        
    except KeyboardInterrupt:
        print("\nShutting down servers...")

if __name__ == "__main__":
    main()