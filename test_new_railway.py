"""Test new Railway deployment with API keys"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Test NEW Railway endpoint
url = "https://langgraph-ai-agent-production-7799.up.railway.app/chat"

data = {
    "message": "What is machine learning?",
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "tavily_api_key": os.getenv("TAVILY_API_KEY")
}

print("🚀 Testing NEW Railway deployment...")
print(f"URL: {url}")
print(f"Message: {data['message']}")
print(f"Has OpenAI key: {bool(data['openai_api_key'])}")
print(f"Has Tavily key: {bool(data['tavily_api_key'])}")

try:
    response = requests.post(url, json=data, timeout=60)
    print(f"\n📊 Response Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS!")
        print(f"Response: {result.get('response', 'No response')[:200]}...")
        print(f"Session ID: {result.get('session_id')}")
        
        # Check for sources
        sources = result.get('sources', [])
        print(f"Sources found: {len(sources)}")
        for i, source in enumerate(sources[:3]):
            print(f"  Source {i+1}: {source.get('title', 'No title')}")
            
    else:
        print("❌ FAILED!")
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"❌ EXCEPTION: {e}")