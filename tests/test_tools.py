"""
Test tools functionality
"""

import pytest
from unittest.mock import Mock, patch
from src.tools.arxiv_search import ArxivSearchTool
from src.tools.helpfulness_checker import HelpfulnessChecker


class TestArxivSearch:
    """Test ArXiv search functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.arxiv_tool = ArxivSearchTool()
    
    @patch('arxiv.Client')
    def test_arxiv_search_success(self, mock_client):
        """Test successful ArXiv search"""
        # Mock paper object
        mock_paper = Mock()
        mock_paper.title = "Test Paper"
        mock_paper.authors = [Mock(name="John Doe")]
        mock_paper.summary = "This is a test paper summary"
        mock_paper.entry_id = "http://arxiv.org/abs/1234.5678"
        mock_paper.published.strftime.return_value = "2023-01-01"
        
        # Mock client results
        mock_client_instance = Mock()
        mock_client_instance.results.return_value = [mock_paper]
        mock_client.return_value = mock_client_instance
        
        results = self.arxiv_tool.search("test query")
        
        assert len(results) == 1
        assert results[0]["title"] == "Test Paper"
        assert results[0]["source"] == "arxiv"
    
    def test_arxiv_get_tool(self):
        """Test getting LangChain tool interface"""
        tool = self.arxiv_tool.get_tool()
        
        assert tool.name == "arxiv_search"
        assert "academic papers" in tool.description.lower()


class TestHelpfulnessChecker:
    """Test helpfulness checker functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.checker = HelpfulnessChecker()
    
    @patch('src.tools.helpfulness_checker.ChatOpenAI')
    def test_helpfulness_evaluation(self, mock_llm):
        """Test helpfulness evaluation"""
        # Mock LLM response
        mock_response = Mock()
        mock_response.content = "0.8"
        
        mock_llm_instance = Mock()
        mock_llm_instance.invoke.return_value = mock_response
        mock_llm.return_value = mock_llm_instance
        
        score = self.checker.evaluate("test query", "test response")
        
        assert score == 0.8
    
    @patch('src.tools.helpfulness_checker.ChatOpenAI')
    def test_helpfulness_evaluation_error(self, mock_llm):
        """Test helpfulness evaluation with error"""
        mock_llm_instance = Mock()
        mock_llm_instance.invoke.side_effect = Exception("API Error")
        mock_llm.return_value = mock_llm_instance
        
        score = self.checker.evaluate("test query", "test response")
        
        assert score == 0.5  # Default score on error