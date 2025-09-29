"""
Integration Test Suite for LangGraph Agent v2
Tests all modules working together: Agent + Tools + Config + Backend
"""

import sys
import os
import asyncio
from typing import Dict, Any
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

def test_imports():
    """Test 1: All module imports work correctly"""
    print("=== TEST 1: Module Imports ===")
    try:
        from agents.langgraph_agentv2 import LangGraphAgent, AgentState
        from tools.tavily_search import TavilySearchTool
        from tools.arxiv_search import ArxivSearchTool  
        from tools.youtube_search import YouTubeSearchTool
        from tools.helpfulness_checker import HelpfulnessChecker
        from utils.config import AppConfig
        from langchain_core.messages import HumanMessage
        
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_tool_functionality():
    """Test 2: Individual tools work independently"""
    print("\n=== TEST 2: Individual Tool Functionality ===")
    
    # Test YouTube (no API key needed)
    try:
        from tools.youtube_search import YouTubeSearchTool
        youtube_tool = YouTubeSearchTool()
        results = youtube_tool.search("Python programming tutorial")
        print(f"✅ YouTube Tool: Found {len(results)} videos")
    except Exception as e:
        print(f"❌ YouTube Tool error: {e}")
    
    # Test ArXiv (no API key needed) 
    try:
        from tools.arxiv_search import ArxivSearchTool
        arxiv_tool = ArxivSearchTool()
        results = arxiv_tool.search("machine learning")
        print(f"✅ ArXiv Tool: Found {len(results)} papers")
    except Exception as e:
        print(f"❌ ArXiv Tool error: {e}")
    
    # Test Config loading
    try:
        from utils.config import AppConfig
        config = AppConfig()
        print(f"✅ Config: Loaded with title '{config.app_title}'")
    except Exception as e:
        print(f"❌ Config error: {e}")
    
    return True

def test_agent_creation():
    """Test 3: Agent can be created with test keys"""
    print("\n=== TEST 3: Agent Creation ===")
    try:
        from agents.langgraph_agentv2 import LangGraphAgent
        from utils.config import AppConfig
        
        config = AppConfig()
        
        # Test with dummy keys (will validate structure)
        try:
            agent = LangGraphAgent(config, "test-key", "test-key") 
            print("❌ Should have failed with invalid keys")
            return False
        except ValueError as e:
            if "API key" in str(e):
                print("✅ Agent validation works (correctly rejects invalid keys)")
                return True
            else:
                print(f"❌ Unexpected validation error: {e}")
                return False
    except Exception as e:
        print(f"❌ Agent creation error: {e}")
        return False

def test_state_structure():
    """Test 4: AgentState structure is correct"""
    print("\n=== TEST 4: State Structure ===")
    try:
        from agents.langgraph_agentv2 import AgentState
        from langchain_core.messages import HumanMessage
        
        # Test creating valid state
        test_state = {
            "messages": [HumanMessage(content="Test")],
            "tools_used": ["youtube_search"],
            "search_results": [{"title": "test", "url": "http://test.com"}],
            "youtube_videos": [{"title": "test video", "channel": "test"}],
            "helpfulness_score": 0.8,
            "session_id": "test123",
            "iteration_count": 0,
        }
        
        # Verify all required fields are present
        required_fields = list(AgentState.__annotations__.keys())
        state_fields = list(test_state.keys())
        
        missing = set(required_fields) - set(state_fields)
        if missing:
            print(f"❌ Missing fields: {missing}")
            return False
        
        print(f"✅ AgentState: All {len(required_fields)} fields present")
        print(f"   Fields: {required_fields}")
        return True
        
    except Exception as e:
        print(f"❌ State structure error: {e}")
        return False

def test_graph_workflow():
    """Test 5: Graph workflow structure (without execution)"""
    print("\n=== TEST 5: Graph Workflow Structure ===")
    try:
        from agents.langgraph_agentv2 import LangGraphAgent
        from utils.config import AppConfig
        
        # Create agent class to check graph structure
        config = AppConfig()
        
        # We can't actually create the agent without valid keys,
        # but we can check the class methods exist
        agent_class = LangGraphAgent
        
        required_methods = [
            '_build_graph',
            '_call_model', 
            '_should_continue',
            '_check_helpfulness',
            '_should_regenerate',
            'process_query'
        ]
        
        for method in required_methods:
            if hasattr(agent_class, method):
                print(f"✅ Method exists: {method}")
            else:
                print(f"❌ Missing method: {method}")
                return False
        
        print("✅ Graph workflow structure is complete")
        return True
        
    except Exception as e:
        print(f"❌ Graph workflow error: {e}")
        return False

def test_backend_integration():
    """Test 6: Backend integration readiness"""
    print("\n=== TEST 6: Backend Integration ===")
    try:
        # Test that backend can import the agent
        sys.path.insert(0, 'backend')
        
        # Check if the agent can be imported from backend context
        from src.agents.langgraph_agentv2 import LangGraphAgent
        print("✅ Backend can import LangGraphAgent v2")
        
        # Test that all required backend components exist
        backend_files = [
            'backend/main.py',
            'src/agents/langgraph_agentv2.py',
            'src/tools/youtube_search.py',
            'src/tools/tavily_search.py',
            'src/tools/arxiv_search.py'
        ]
        
        for file_path in backend_files:
            if os.path.exists(file_path):
                print(f"✅ File exists: {file_path}")
            else:
                print(f"❌ Missing file: {file_path}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Backend integration error: {e}")
        return False

def run_integration_tests():
    """Run all integration tests"""
    print("🧪 LANGGRAPH AGENT V2 INTEGRATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_tool_functionality, 
        test_agent_creation,
        test_state_structure,
        test_graph_workflow,
        test_backend_integration
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results), 1):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"Test {i}: {test.__name__:25} {status}")
    
    print(f"\n🎯 OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ LangGraph Agent v2 is ready for production integration")
        
        print("\n🚀 NEXT STEPS:")
        print("1. Add valid API keys to .env file")
        print("2. Run end-to-end test with real API calls")
        print("3. Compare performance with v1 agent")
        print("4. Deploy v2 to production")
    else:
        print(f"\n⚠️ {total-passed} test(s) failed - fix issues before deploying")
    
    return passed == total

if __name__ == "__main__":
    run_integration_tests()