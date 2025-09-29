#!/usr/bin/env python3
"""
Test the full agent with YouTube integration
"""
import sys
import os
sys.path.append('src')

try:
    from src.agents.langgraph_agent import LangGraphAgent
    from src.utils.config import AppConfig
    
    # Create dummy config
    class DummyConfig:
        def __init__(self):
            self.openai_api_key = "dummy-key"
            self.tavily_api_key = "dummy-key"
    
    config = DummyConfig()
    
    # Create agent
    agent = LangGraphAgent(
        config=config,
        openai_api_key="dummy-key",
        tavily_api_key="dummy-key"
    )
    
    print('✅ Agent created successfully!')
    print('📊 Testing query analysis...')
    
    # Test query that should trigger YouTube search
    test_query = "How to learn Python programming step by step"
    
    # Test the analysis function directly
    test_state = {
        "query": test_query,
        "messages": [],
        "response": "",
        "tools_used": [],
        "search_results": [],
        "youtube_videos": [],
        "helpfulness_score": None,
        "session_id": "test",
        "iteration_count": 0,
        "needs_web_search": False,
        "needs_arxiv_search": False,
        "needs_youtube_search": False
    }
    
    # Test analysis
    analyzed_state = agent._analyze_query(test_state)
    
    print(f"🔍 Analysis results:")
    print(f"   - Web search needed: {analyzed_state.get('needs_web_search')}")
    print(f"   - ArXiv search needed: {analyzed_state.get('needs_arxiv_search')}")
    print(f"   - YouTube search needed: {analyzed_state.get('needs_youtube_search')}")
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()