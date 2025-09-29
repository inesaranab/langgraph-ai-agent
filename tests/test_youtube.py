#!/usr/bin/env python3
"""
Test YouTube integration
"""
import sys
import os
sys.path.append('src')

try:
    from src.tools.youtube_search import YouTubeSearchTool
    yt_tool = YouTubeSearchTool()
    results = yt_tool.search('how to learn python programming')
    print('✅ YouTube search working!')
    print(f'Found {len(results)} videos')
    for video in results:
        print(f'- {video["title"]}')
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()