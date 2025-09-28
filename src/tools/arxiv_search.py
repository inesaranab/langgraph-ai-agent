"""
ArXiv Search Tool Integration
Provides academic paper search capabilities using ArXiv API
"""

import arxiv
from typing import List, Dict, Any
from langchain.tools import Tool


class ArxivSearchTool:
    """ArXiv search tool for academic papers"""
    
    def __init__(self):
        self.client = arxiv.Client()
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search ArXiv for academic papers"""
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = []
            for paper in self.client.results(search):
                results.append({
                    "title": paper.title,
                    "authors": [author.name for author in paper.authors],
                    "summary": paper.summary,
                    "url": paper.entry_id,
                    "published": paper.published.strftime("%Y-%m-%d"),
                    "content": f"{paper.title}\n\nAuthors: {', '.join([author.name for author in paper.authors])}\n\nSummary: {paper.summary[:500]}...",
                    "snippet": paper.summary[:300] + "..." if len(paper.summary) > 300 else paper.summary,
                    "source": "arxiv"
                })
            
            return results
            
        except Exception as e:
            print(f"ArXiv search error: {e}")
            return []
    
    def get_tool(self) -> Tool:
        """Get LangChain tool interface"""
        return Tool(
            name="arxiv_search",
            description="Search ArXiv for academic papers and research. Use this for scientific research, academic studies, and scholarly articles.",
            func=lambda query: self.search(query)
        )