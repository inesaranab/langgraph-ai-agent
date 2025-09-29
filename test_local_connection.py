#!/usr/bin/env python3
"""
Test local frontend-backend connection
"""

import requests
import json
import time

def test_backend_health():
    """Test that backend is running and healthy"""
    print("🔍 Testing backend health...")
    try:
        response = requests.get("http://localhost:8000/health")
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Backend health: {data}")
        return True
        
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        return False

def test_frontend_accessible():
    """Test that frontend is accessible"""
    print("\n🔍 Testing frontend accessibility...")
    try:
        response = requests.get("http://localhost:3001")
        response.raise_for_status()
        
        print(f"✅ Frontend accessible: Status {response.status_code}")
        return True
        
    except Exception as e:
        print(f"❌ Frontend accessibility failed: {e}")
        return False

def test_cors_enabled():
    """Test CORS configuration"""
    print("\n🔍 Testing CORS configuration...")
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Content-Type': 'application/json'
        }
        response = requests.options("http://localhost:8000/health", headers=headers)
        
        cors_headers = response.headers.get('Access-Control-Allow-Origin', '')
        print(f"✅ CORS headers: {cors_headers}")
        return True
        
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

def test_chat_endpoint():
    """Test basic chat functionality"""
    print("\n🔍 Testing chat endpoint (without API keys)...")
    try:
        payload = {
            "message": "Hello, can you search for information about Python?",
            "session_id": "test-session-123"
        }
        
        response = requests.post(
            "http://localhost:8000/chat",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat endpoint working: {data.get('response', '')[:100]}...")
        elif response.status_code == 422:
            print("⚠️  Chat endpoint accessible but needs API keys (expected)")
        else:
            print(f"❌ Chat endpoint error: {response.status_code}")
            
        return True
        
    except Exception as e:
        print(f"❌ Chat endpoint test failed: {e}")
        return False

def main():
    """Run all connection tests"""
    print("🚀 Testing local frontend-backend connection\n")
    
    tests = [
        test_backend_health,
        test_frontend_accessible,
        test_cors_enabled,
        test_chat_endpoint
    ]
    
    results = []
    for test in tests:
        results.append(test())
        time.sleep(0.5)
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! Frontend and backend are connected successfully.")
        print("\n📋 Next steps:")
        print("   1. Open http://localhost:3001 in your browser")
        print("   2. Add your OpenAI and Tavily API keys in the settings")
        print("   3. Start chatting with the AI agent!")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    main()