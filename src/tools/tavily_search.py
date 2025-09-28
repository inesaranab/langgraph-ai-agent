"""
Tavily Search Tool Integration
Provides web search capabilities using Tavily API
"""

import os
from typing import List, Dict, Any, Optional
from tavily import TavilyClient
from langchain.tools import Tool


class TavilySearchTool:
    """Tavily search tool for web search capabilities"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not provided and not found in environment variables")
        
        self.client = TavilyClient(api_key=self.api_key)
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Perform web search using Tavily"""
        try:
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_images=False,
                include_answer=True
            )
            
            results = []
            for result in response.get("results", []):
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "snippet": result.get("content", "")[:300] + "..." if len(result.get("content", "")) > 300 else result.get("content", ""),
                    "source": "web"
                })
            
            return results
            
        except Exception as e:
            print(f"Tavily search error: {e}")
            return []
    
    def get_tool(self) -> Tool:
        """Get LangChain tool interface"""
        return Tool(
            name="web_search",
            description="Search the web for current information, news, and general knowledge. Use this for recent events, current affairs, and up-to-date information.",
            func=lambda query: self.search(query)
        )