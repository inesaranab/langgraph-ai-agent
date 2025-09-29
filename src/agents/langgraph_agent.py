"""
LangGraph Agent Implementation
Core agent logic with tool integration and state management
"""

import time
from typing import Dict, List, Any, Optional
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
import uuid

from tools.tavily_search import TavilySearchTool
from tools.arxiv_search import ArxivSearchTool
from tools.youtube_search import YouTubeSearchTool
from tools.helpfulness_checker import HelpfulnessChecker
from utils.config import AppConfig


class AgentState(TypedDict):
    """State definition for the agent"""
    messages: List[Any]
    query: str
    response: str
    tools_used: List[str]
    search_results: List[Dict]
    youtube_videos: List[Dict]
    helpfulness_score: Optional[float]
    session_id: str
    iteration_count: int
    needs_web_search: bool
    needs_arxiv_search: bool
    needs_youtube_search: bool


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
        
        # Build the graph
        self.graph = self._build_graph()
        
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyzer", self._analyze_query)
        workflow.add_node("tool_caller", self._call_tools)
        workflow.add_node("responder", self._generate_response)
        workflow.add_node("helpfulness_checker", self._check_helpfulness)
        
        # Add edges
        workflow.set_entry_point("analyzer")
        workflow.add_conditional_edges(
            "analyzer",
            self._should_use_tools,
            {
                "use_tools": "tool_caller",
                "direct_response": "responder"
            }
        )
        workflow.add_edge("tool_caller", "responder")
        workflow.add_edge("responder", "helpfulness_checker")
        workflow.add_conditional_edges(
            "helpfulness_checker",
            self._should_regenerate,
            {
                "regenerate": "responder",
                "finish": END
            }
        )
        
        return workflow.compile()
    
    def _analyze_query(self, state: AgentState) -> AgentState:
        """Analyze the user query to determine next steps"""
        query = state["query"]
        
        try:
            query_lower = query.lower()
            
            # More inclusive criteria for web search - most queries benefit from current information
            needs_web_search = any(word in query_lower for word in [
                "news", "current", "recent", "today", "latest", "what's happening",
                "weather", "stock", "price", "trends", "developments", "updates",
                "companies", "technology", "AI", "artificial intelligence"
            ]) or len(query.split()) > 3  # Complex queries likely need web search
            
            # Search for academic content when specifically requested or for research topics
            needs_arxiv_search = any(word in query_lower for word in [
                "research", "paper", "study", "academic", "scientific", 
                "arxiv", "journal", "publication", "algorithm", "machine learning"
            ])
            
            # Search for YouTube videos when users want tutorials, explanations, or learning content
            needs_youtube_search = any(word in query_lower for word in [
                "how to", "tutorial", "learn", "explain", "show me", "teach", 
                "guide", "demonstration", "example", "video", "watch", "course",
                "lesson", "training", "instructions", "walkthrough", "beginner"
            ]) or any(phrase in query_lower for phrase in [
                "step by step", "getting started", "for beginners"
            ])
            
            state["needs_web_search"] = needs_web_search
            state["needs_arxiv_search"] = needs_arxiv_search
            state["needs_youtube_search"] = needs_youtube_search
            

        except Exception as e:
            print(f"Analysis error: {e}")
            state["needs_web_search"] = False
            state["needs_arxiv_search"] = False
            state["needs_youtube_search"] = False
            
        return state
    
    def _should_use_tools(self, state: AgentState) -> str:
        """Decide whether to use tools or respond directly"""
        if state.get("needs_web_search") or state.get("needs_arxiv_search") or state.get("needs_youtube_search"):
            return "use_tools"
        return "direct_response"
    
    def _call_tools(self, state: AgentState) -> AgentState:
        """Execute relevant tools based on analysis"""
        query = state["query"]
        search_results = []
        tools_used = []
        
        # Web search if needed
        if state.get("needs_web_search"):
            try:
                web_results = self.tavily_tool.search(query)
                search_results.extend(web_results)
                tools_used.append("web_search")
            except Exception as e:
                print(f"Web search error: {e}")
        
        # ArXiv search if needed
        if state.get("needs_arxiv_search"):
            try:
                arxiv_results = self.arxiv_tool.search(query)
                search_results.extend(arxiv_results)
                tools_used.append("arxiv_search")
            except Exception as e:
                print(f"ArXiv search error: {e}")
        
        # YouTube search if needed
        youtube_videos = []
        if state.get("needs_youtube_search"):
            try:
                youtube_results = self.youtube_tool.search(query, max_results=3)
                youtube_videos = youtube_results
                # Also add to search_results for unified processing
                search_results.extend(youtube_results)
                tools_used.append("youtube_search")
            except Exception as e:
                print(f"YouTube search error: {e}")
        
        state["search_results"] = search_results
        state["youtube_videos"] = youtube_videos
        state["tools_used"] = tools_used
        
        return state
    
    def _generate_response(self, state: AgentState) -> AgentState:
        """Generate the final response"""
        query = state["query"]
        search_results = state.get("search_results", [])
        
        # Create context from search results
        context = ""
        if search_results:
            context = "\n\nRelevant information:\n"
            for i, result in enumerate(search_results[:5], 1):
                context += f"{i}. {result.get('title', 'N/A')}: {result.get('content', result.get('snippet', 'No content'))}\n"
        
        # Generate response
        system_message = """You are a helpful AI assistant. Provide comprehensive, accurate, and helpful responses. 
        If you have search results, incorporate them naturally into your response while citing sources when appropriate.
        Be conversational but informative."""
        
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=f"Query: {query}{context}")
        ]
        
        try:
            response = self.llm.invoke(messages)
            state["response"] = str(response.content) if hasattr(response.content, '__str__') else str(response.content)
        except Exception as e:
            state["response"] = f"I apologize, but I encountered an error while generating a response: {str(e)}"
        
        return state
    
    def _check_helpfulness(self, state: AgentState) -> AgentState:
        """Check if the response is helpful"""
        try:
            score = self.helpfulness_checker.evaluate(
                state["query"], 
                state["response"]
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
        
        # Initial state
        initial_state: AgentState = {
            "messages": [],
            "query": query,
            "response": "",
            "tools_used": [],
            "search_results": [],
            "youtube_videos": [],
            "helpfulness_score": None,
            "session_id": session_id,
            "iteration_count": 0,
            "needs_web_search": False,
            "needs_arxiv_search": False,
            "needs_youtube_search": False
        }
        
        try:
            # Execute the graph
            final_state = self.graph.invoke(initial_state)
            
            processing_time = time.time() - start_time
            
            # Format sources for frontend
            sources = []
            search_results = final_state.get("search_results", [])
            for result in search_results:
                source = {
                    "title": result.get("title", "Unknown Title"),
                    "url": result.get("url", ""),
                    "snippet": result.get("content", result.get("snippet", "No preview available"))[:200] + "...",
                    "type": "arxiv" if "arxiv.org" in result.get("url", "") else "web",
                    "published_date": result.get("published_date", result.get("date")),
                    "score": result.get("score", 0.5)
                }
                sources.append(source)
            
            metadata = {
                "tools_used": final_state.get("tools_used", []),
                "processing_time": processing_time,
                "helpfulness_score": final_state.get("helpfulness_score"),
                "search_results_count": len(search_results),
                "session_id": session_id,
                "sources": sources[:10]  # Limit to top 10 sources
            }
            
            return {
                "response": final_state.get("response", "No response generated"),
                "metadata": metadata,
                "tools_used": final_state.get("tools_used", []),
                "youtube_videos": len(final_state.get("youtube_videos", [])),
                "search_results": len(final_state.get("search_results", []))
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