"""
Application Configuration
Handles app settings and environment variables
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class AppConfig:
    """Application configuration settings"""
    
    # API Keys
    openai_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    langchain_api_key: Optional[str] = None
    
    # App Settings
    app_title: str = "LangGraph AI Agent"
    app_description: str = "Intelligent AI agent powered by LangGraph"
    debug: bool = False
    
    # FastAPI Settings
    fastapi_port: int = 8000
    fastapi_host: str = "0.0.0.0"
    
    # LangChain Settings
    langchain_tracing: bool = False
    langchain_project: str = "langgraph-agent-app"
    
    def __post_init__(self):
        """Load configuration from environment variables"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
        
        self.app_title = os.getenv("APP_TITLE", self.app_title)
        self.app_description = os.getenv("APP_DESCRIPTION", self.app_description)
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        
        self.fastapi_port = int(os.getenv("FASTAPI_SERVER_PORT", self.fastapi_port))
        self.fastapi_host = os.getenv("FASTAPI_SERVER_ADDRESS", self.fastapi_host)
        
        self.langchain_tracing = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
        self.langchain_project = os.getenv("LANGCHAIN_PROJECT", self.langchain_project)
        
        # Set environment variables for LangChain
        if self.openai_api_key:
            os.environ["OPENAI_API_KEY"] = self.openai_api_key
        if self.langchain_api_key:
            os.environ["LANGCHAIN_API_KEY"] = self.langchain_api_key
        if self.langchain_tracing:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
        if self.langchain_project:
            os.environ["LANGCHAIN_PROJECT"] = self.langchain_project
    
    def validate(self) -> bool:
        """Validate required configuration"""
        if not self.openai_api_key:
            print("Warning: OPENAI_API_KEY not set")
            return False
        
        if not self.tavily_api_key:
            print("Warning: TAVILY_API_KEY not set")
            return False
        
        return True
    
    def get_required_env_vars(self) -> list:
        """Get list of required environment variables"""
        return [
            "OPENAI_API_KEY",
            "TAVILY_API_KEY"
        ]