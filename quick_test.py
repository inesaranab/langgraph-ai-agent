import requests
import json

# Test backend
print("Testing backend...")
try:
    response = requests.get("http://localhost:8000/health")
    print(f"✅ Backend: {response.json()}")
except Exception as e:
    print(f"❌ Backend: {e}")

# Test frontend
print("\nTesting frontend...")
try:
    response = requests.get("http://localhost:3001", timeout=5)
    print(f"✅ Frontend: Status {response.status_code}")
except Exception as e:
    print(f"❌ Frontend: {e}")

# Test CORS
print("\nTesting CORS...")
try:
    headers = {'Origin': 'http://localhost:3001'}
    response = requests.options("http://localhost:8000/health", headers=headers)
    cors = response.headers.get('Access-Control-Allow-Origin', 'None')
    print(f"✅ CORS: {cors}")
except Exception as e:
    print(f"❌ CORS: {e}")

print("\n🎉 Frontend: http://localhost:3001")
print("🎉 Backend: http://localhost:8000")