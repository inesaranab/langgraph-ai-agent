"""
Test configuration for the application
"""

import pytest
import os
from src.utils.config import AppConfig


class TestConfig:
    """Test application configuration"""
    
    def test_config_initialization(self):
        """Test config initialization with default values"""
        config = AppConfig()
        
        assert config.app_title == "LangGraph AI Agent"
        assert config.fastapi_port == 8000
        assert config.debug == False
    
    def test_config_from_env(self, monkeypatch):
        """Test config loading from environment variables"""
        monkeypatch.setenv("APP_TITLE", "Test App")
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("FASTAPI_SERVER_PORT", "9000")
        
        config = AppConfig()
        
        assert config.app_title == "Test App"
        assert config.debug == True
        assert config.fastapi_port == 9000
    
    def test_config_validation(self):
        """Test configuration validation"""
        config = AppConfig()
        
        # Should fail without API keys
        assert config.validate() == False
    
    def test_required_env_vars(self):
        """Test required environment variables list"""
        config = AppConfig()
        required_vars = config.get_required_env_vars()
        
        assert "OPENAI_API_KEY" in required_vars
        assert "TAVILY_API_KEY" in required_vars