import re
import requests
import os
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def extract_video_id(url: str) -> Optional[str]:
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_info(video_id: str) -> Optional[Dict]:
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY not found in environment variables")
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        'part': 'snippet',
        'id': video_id,
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    data = response.json()
    if not data.get('items'):
        return None
    video = data['items'][0]
    snippet = video['snippet']
    return {
        'title': snippet.get('title', ''),
        'description': snippet.get('description', ''),
        'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url', '')
    }
