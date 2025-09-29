#!/usr/bin/env python3
"""
Debug frontend-backend 404 issue
"""

import requests

# Test all backend endpoints
BACKEND_URL = "https://langgraph-ai-agent-production-561e.up.railway.app"

endpoints_to_test = [
    "/",
    "/health", 
    "/chat",
    "/docs",
    "/openapi.json"
]

print(f"Testing backend endpoints on: {BACKEND_URL}")
print("=" * 60)

for endpoint in endpoints_to_test:
    try:
        url = f"{BACKEND_URL}{endpoint}"
        response = requests.get(url, timeout=10)
        print(f"✅ {endpoint:<15} -> {response.status_code} {response.reason}")
        
        if endpoint == "/health":
            data = response.json()
            print(f"   Status: {data.get('status')}")
            
    except Exception as e:
        print(f"❌ {endpoint:<15} -> ERROR: {e}")

print("\n" + "=" * 60)
print("Testing CORS with frontend origin...")

try:
    headers = {
        'Origin': 'https://myfirstadvanced-46vjx23bi-inesaranabs-projects.vercel.app',
        'Content-Type': 'application/json'
    }
    
    # Test preflight request
    response = requests.options(f"{BACKEND_URL}/health", headers=headers)
    print(f"OPTIONS /health -> {response.status_code}")
    print(f"CORS headers: {response.headers.get('Access-Control-Allow-Origin', 'None')}")
    
    # Test actual request
    response = requests.get(f"{BACKEND_URL}/health", headers=headers)
    print(f"GET /health -> {response.status_code}")
    
except Exception as e:
    print(f"CORS test failed: {e}")

print(f"\n🌐 Frontend: https://myfirstadvanced-46vjx23bi-inesaranabs-projects.vercel.app")
print(f"🔗 Backend: {BACKEND_URL}")

print("\n💡 To debug in browser:")
print("1. Open frontend URL")
print("2. Press F12 -> Network tab")
print("3. Look for failed requests (red entries)")
print("4. Click on failed request to see details")