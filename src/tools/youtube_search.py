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
            
            # Search for videos using youtube_search
            results = self.youtube_search(enhanced_query, max_results=max_results).to_dict()
            
            formatted_results = []
            for video in results:
                # Ensure video is a dictionary
                if not isinstance(video, dict):
                    continue
                # Extract video information
                video_info = {
                    "title": video.get("title", "Unknown Title"),
                    "url": f"https://www.youtube.com{video.get('url_suffix', '')}",
                    "channel": video.get("channel", "Unknown Channel"),
                    "duration": video.get("duration", "Unknown Duration"),
                    "views": video.get("views", "Unknown Views"),
                    "description": (video.get("long_desc") or "No description available")[:200] + "...",
                    "thumbnail": video.get("thumbnails", [""])[0] if video.get("thumbnails") else "",
                    "source": "youtube",
                    "type": "educational_video"
                }
                formatted_results.append(video_info)
                
            print(f"[SUCCESS] Found {len(formatted_results)} YouTube videos for: {query}")
            return formatted_results
            
        except Exception as e:
            print(f"[ERROR] YouTube search error: {e}")
            return []
    
    def get_tool(self) -> Tool:
        """Get LangChain tool interface"""
        return Tool(
            name="youtube_search",
            description="Search YouTube for educational videos, tutorials, and explanations. Use this to find video content that helps users learn more about the topic.",
            func=lambda query: self.search(query)
        )
    
    def format_videos_for_response(self, videos: List[Dict[str, Any]], topic: str) -> str:
        """Format videos into a learn-more appendix"""
        if not videos:
            return ""
        
        appendix = f"\n\n## Learn More: Video Resources about '{topic}'\n\n"
        
        for i, video in enumerate(videos, 1):
            appendix += f"**{i}. {video['title']}**\n"
            appendix += f"   Channel: {video['channel']}\n"
            appendix += f"   Duration: {video['duration']}\n"
            appendix += f"   [Watch Video]({video['url']})\n"
            
            # Add description if available and meaningful
            desc = video.get('description', '').strip()
            if desc and len(desc) > 20:
                appendix += f"   Description: {desc}\n"
            
            appendix += "\n"
        
        return appendix