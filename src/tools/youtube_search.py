"""
YouTube Search Tool Integration
Provides video search capabilities for educational content
"""

import os
from typing import List, Dict, Any, Optional
from langchain.tools import Tool


class YouTubeSearchTool:
    """YouTube search tool for educational video content"""
    
    def __init__(self):
        """Initialize YouTube search tool"""
        # Note: Using youtube_search package which doesn't require API key
        try:
            from youtube_search import YoutubeSearch
            self.youtube_search = YoutubeSearch
        except ImportError:
            raise ImportError(
                "youtube_search package not installed. "
                "Install with: pip install youtube-search"
            )
    
    def search(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """Search YouTube for educational videos"""
        try:
            # Enhance query for better educational results
            enhanced_query = f"{query} tutorial explanation"
            
            # Search YouTube
            results = self.youtube_search(enhanced_query, max_results=max_results).to_dict()
            
            videos = []
            for video in results:
                # Handle description safely
                long_desc = video.get("long_desc") or "No description available"
                description = long_desc[:200] + "..." if len(long_desc) > 200 else long_desc
                
                # Handle thumbnail safely
                thumbnails = video.get("thumbnails", [])
                thumbnail_url = thumbnails[0] if thumbnails else ""
                
                video_data = {
                    "title": video.get("title", "Unknown Title"),
                    "url": f"https://www.youtube.com{video.get('url_suffix', '')}",
                    "description": description,
                    "duration": video.get("duration", "Unknown"),
                    "channel": video.get("channel", "Unknown Channel"),
                    "published_date": video.get("publish_time", "Unknown"),
                    "thumbnail": thumbnail_url,
                    "views": video.get("views", "Unknown"),
                    "type": "youtube",
                    "score": 0.8  # High score for educational content
                }
                videos.append(video_data)
                
            return videos
            
        except Exception as e:
            print(f"YouTube search error: {e}")
            return []
    
    def get_tool(self) -> Tool:
        """Get the LangChain tool for YouTube search"""
        return Tool(
            name="youtube_search",
            description=(
                "Search YouTube for educational videos, tutorials, and explanations. "
                "Use this when users want to learn about topics through video content. "
                "Input should be a search query string."
            ),
            func=self._tool_search
        )
    
    def _tool_search(self, query: str) -> str:
        """Tool function for LangChain integration"""
        try:
            videos = self.search(query, max_results=3)
            if not videos:
                return "No YouTube videos found for the given query."
            
            result = f"Found {len(videos)} educational YouTube videos:\n\n"
            
            for i, video in enumerate(videos, 1):
                result += f"{i}. **{video['title']}**\n"
                result += f"   Channel: {video['channel']}\n"
                result += f"   Duration: {video['duration']}\n"
                result += f"   URL: {video['url']}\n"
                result += f"   Description: {video['description']}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error searching YouTube: {str(e)}"