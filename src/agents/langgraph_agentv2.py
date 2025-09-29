"""
LangGraph Agent Implementation v2
Simplified agent logic with tool integration and state management
"""

import time
import json
from typing import Dict, List, Any, Optional, TypedDict, Annotated
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, END
import uuid

from src.tools.tavily_search import TavilySearchTool
from src.tools.arxiv_search import ArxivSearchTool
from src.tools.youtube_search import YouTubeSearchTool
from src.tools.helpfulness_checker import HelpfulnessChecker
from src.utils.config import AppConfig


class AgentState(TypedDict):
    """State definition for the agent"""
    messages: Annotated[list, add_messages]
    tools_used: List[str]
    search_results: List[Dict]
    youtube_videos: List[Dict]
    helpfulness_score: Optional[float]
    session_id: str
    iteration_count: int


class LangGraphAgent:
    """Main LangGraph agent with tool integration"""
    
    def __init__(self, config: AppConfig, openai_api_key: Optional[str] = None, tavily_api_key: Optional[str] = None):
        self.config = config
        self.openai_api_key = openai_api_key or config.openai_api_key
        self.tavily_api_key = tavily_api_key or config.tavily_api_key
        
        # Validate required API keys
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass openai_api_key parameter.")
        
        if not self.tavily_api_key:
            raise ValueError("Tavily API key is required. Set TAVILY_API_KEY environment variable or pass tavily_api_key parameter.")
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            streaming=True,
            api_key=SecretStr(self.openai_api_key)
        )
        
        # Initialize tools with dynamic API keys
        self.tavily_tool = TavilySearchTool(api_key=self.tavily_api_key)
        self.arxiv_tool = ArxivSearchTool()
        self.youtube_tool = YouTubeSearchTool()
        self.helpfulness_checker = HelpfulnessChecker(api_key=self.openai_api_key)
        
        # Available tools
        self.tools = [
            self.tavily_tool.get_tool(),
            self.arxiv_tool.get_tool(),
            self.youtube_tool.get_tool()
        ]

        # Model with tools
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        # Tool Node
        self._tool_node = ToolNode(self.tools)
        
        # Build the graph
        self.graph = self._build_graph()
        
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", self._call_model)
        workflow.add_node("action", self._tool_node)
        workflow.add_node("helpfulness_checker", self._check_helpfulness)
        
        # Add edges
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            self._should_continue
        )
        workflow.add_edge("action", "agent")
        workflow.add_conditional_edges(
            "helpfulness_checker",
            self._should_regenerate,
            {
                "regenerate": "agent",
                "finish": END
            }
        )
        
        return workflow.compile()
    
    def _call_model(self, state: AgentState):
        """Call LLM with automatic tool selection"""
        messages = state["messages"]
        response = self.llm_with_tools.invoke(messages)
        return {'messages': [response]}
    
    def _should_continue(self, state: AgentState) -> str:
        """Decide whether to use tools or check helpfulness"""
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "action"
        return "helpfulness_checker"
    
    def _check_helpfulness(self, state: AgentState) -> AgentState:
        """Check if the response is helpful"""
        try:
            score = self.helpfulness_checker.evaluate(
                state["messages"][-1], 
                state["messages"][0]
            )
            state["helpfulness_score"] = score
        except Exception as e:
            print(f"Helpfulness check error: {e}")
            state["helpfulness_score"] = 0.5  # Default neutral score
        
        return state
    
    def _should_regenerate(self, state: AgentState) -> str:
        """Decide whether to regenerate response based on helpfulness"""
        helpfulness_score = state.get("helpfulness_score", 0.5)
        iteration_count = state.get("iteration_count", 0)
        
        # Regenerate if score is low and we haven't tried too many times
        if helpfulness_score is not None and helpfulness_score < 0.3 and iteration_count < 2:
            state["iteration_count"] = iteration_count + 1
            return "regenerate"
        
        return "finish"
    
    def process_query(self, query: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a user query and return response with metadata"""
        start_time = time.time()
        
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Initial state - FIXED: Added user query as HumanMessage
        initial_state: AgentState = {
            "messages": [HumanMessage(content=query)],
            "tools_used": [],
            "search_results": [],
            "youtube_videos": [],
            "helpfulness_score": None,
            "session_id": session_id,
            "iteration_count": 0,
        }
        
        try:
            # Execute the graph
            final_state = self.graph.invoke(initial_state)
            
            processing_time = time.time() - start_time
            
            # Format sources for frontend - FIXED: Extract from ToolMessage content
            sources = []
            search_results = []
            youtube_videos = []
            
            # Extract search results from ToolMessage content in messages
            messages = final_state.get("messages", [])
            for message in messages:
                if hasattr(message, 'content') and message.content and hasattr(message, 'type') and message.type == 'tool':
                    try:
                        content = str(message.content)
                        # Try to parse JSON content from tool messages
                        if content.startswith('[') and content.endswith(']'):
                            tool_data = json.loads(content)
                            if isinstance(tool_data, list):
                                search_results.extend(tool_data)
                        elif content.startswith('{') and content.endswith('}'):
                            tool_data = json.loads(content)
                            if isinstance(tool_data, dict):
                                search_results.append(tool_data)
                    except (json.JSONDecodeError, AttributeError):
                        # If not JSON, skip this message
                        continue
            
            print(f"DEBUG: Extracted {len(search_results)} search results from ToolMessages")
            
            # Add search results (web and arxiv)
            for result in search_results:
                print(f"DEBUG: Processing result: {result.get('title', 'No title')}")
                source = {
                    "title": result.get("title", "Unknown Title"),
                    "url": result.get("url", ""),
                    "snippet": result.get("content", result.get("snippet", "No preview available"))[:200] + "...",
                    "type": "arxiv" if "arxiv.org" in result.get("url", "") else "web",
                    "published_date": result.get("published_date", result.get("date")),
                    "score": result.get("score", 0.5)
                }
                sources.append(source)
            
            # Add YouTube videos as sources (from state - these may still work)
            youtube_videos = final_state.get("youtube_videos", [])
            for video in youtube_videos:
                print(f"DEBUG: Processing YouTube video: {video.get('title', 'No title')}")
                source = {
                    "title": video.get("title", "Unknown Title"),
                    "url": video.get("url", ""),
                    "snippet": video.get("description", "No description available"),
                    "type": "youtube",
                    "published_date": video.get("published_date"),
                    "score": 0.8,  # High score for educational videos
                    "duration": video.get("duration", "Unknown"),
                    "channel": video.get("channel", "Unknown Channel"),
                    "thumbnail": video.get("thumbnail", "")
                }
                sources.append(source)
            
            print(f"DEBUG: Formatted {len(sources)} sources for frontend")

            metadata = {
                "tools_used": final_state.get("tools_used", []),
                "processing_time": processing_time,
                "helpfulness_score": final_state.get("helpfulness_score"),
                "search_results_count": len(search_results),
                "session_id": session_id,
                "sources": sources[:10]  # Limit to top 10 sources
            }
            
            print(f"DEBUG: Final metadata includes {len(metadata.get('sources', []))} sources")
            
            # FIXED: Extract response from messages instead of non-existent 'response' key
            return {
                "response": final_state["messages"][-1].content if final_state["messages"] else "No response generated",
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "response": f"I encountered an error while processing your request: {str(e)}",
                "metadata": {
                    "error": str(e),
                    "processing_time": time.time() - start_time,
                    "session_id": session_id
                }
            }