import asyncio
import aiohttp
import yt_dlp
from typing import Dict, Any, Optional
import hashlib
from datetime import datetime
import json
import os
import config

class UnifiedExtractor:
    """Extracts content using multiple strategies"""
    
    def __init__(self):
        self.strategies = {
            'ytdlp': YTDLPStrategy(),
        }
        self.stats = {name: {'success': 0, 'fail': 0} for name in self.strategies}
        
    async def extract(self, url: str) -> Dict[str, Any]:
        """Try all strategies until one works"""
        
        # Try strategies in order
        for strategy_name, strategy in self.strategies.items():
            try:
                print(f"Trying {strategy_name}...")
                result = await strategy.download(url)
                
                # Update stats
                self.stats[strategy_name]['success'] += 1
                
                return {
                    'success': True,
                    'strategy': strategy_name,
                    'data': result,
                    'timestamp': datetime.now().isoformat()
                }
                
            except Exception as e:
                print(f"{strategy_name} failed: {str(e)}")
                self.stats[strategy_name]['fail'] += 1
                continue
        
        return {
            'success': False,
            'error': 'All strategies failed',
            'stats': self.stats
        }
    
    async def process(self, raw_result: Dict) -> Dict:
        """Process raw result into final format"""
        if not raw_result['success']:
            raise Exception(raw_result['error'])
        
        data = raw_result['data']
        
        return {
            'type': 'video' if data.get('is_video', False) else 'photo',
            'data': data['content'],
            'caption': data.get('caption', ''),
            'metadata': {
                'url': data.get('url', ''),
                'author': data.get('author', ''),
                'timestamp': data.get('timestamp', ''),
                'strategy': raw_result['strategy']
            }
        }

class YTDLPStrategy:
    async def download(self, url: str) -> Dict:
        """Download using yt-dlp with cookies - supports reels, posts, and stories"""
        
        # Check for cookies file
        cookies_file = None
        if os.path.exists('instagram_cookies.txt'):
            cookies_file = 'instagram_cookies.txt'
            print(f"Using cookies from {cookies_file}")
        elif os.path.exists('cookies/instagram_cookies.txt'):
            cookies_file = 'cookies/instagram_cookies.txt'
            print(f"Using cookies from {cookies_file}")
        
        # Detect if it's a story URL
        is_story = '/stories/' in url
        
        # Base options
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'outtmpl': 'temp/%(id)s.%(ext)s',
        }
        
        # Different format selection based on content type
        if is_story:
            print("Detected Instagram story, using story-specific settings...")
            ydl_opts['format'] = 'best'  # Stories are simpler
        else:
            ydl_opts['format'] = 'best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'
        
        # Add cookies if available
        if cookies_file:
            ydl_opts['cookiefile'] = cookies_file
        elif config.INSTAGRAM_USERNAME and config.INSTAGRAM_PASSWORD:
            ydl_opts['username'] = config.INSTAGRAM_USERNAME
            ydl_opts['password'] = config.INSTAGRAM_PASSWORD
        
        # Ensure temp directory exists
        os.makedirs('temp', exist_ok=True)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # For stories, we might need to extract playlist info
                if is_story:
                    try:
                        # First try to extract info without downloading
                        info = ydl.extract_info(url, download=False)
                        
                        # If it's a playlist (multiple story items)
                        if 'entries' in info:
                            print(f"Story has {len(info['entries'])} items")
                            # Download the first item (you can modify to download all)
                            if info['entries']:
                                first_entry = info['entries'][0]
                                story_url = first_entry.get('webpage_url', url)
                                info = ydl.extract_info(story_url, download=True)
                        else:
                            info = ydl.extract_info(url, download=True)
                    except Exception as story_error:
                        print(f"Story extraction error: {story_error}")
                        # Fallback to regular download
                        info = ydl.extract_info(url, download=True)
                else:
                    # Regular download for reels/posts
                    info = ydl.extract_info(url, download=True)
                
                # Get file path
                filename = ydl.prepare_filename(info)
                
                # Check if file exists
                if not os.path.exists(filename):
                    # Try to find any video file in temp
                    for file in os.listdir('temp'):
                        if file.endswith(('.mp4', '.mkv', '.webm', '.jpg', '.jpeg', '.png')):
                            filename = os.path.join('temp', file)
                            break
                
                # Read file
                with open(filename, 'rb') as f:
                    content = f.read()
                
                # Determine content type
                is_video = filename.endswith(('.mp4', '.mkv', '.webm'))
                
                # Clean up
                try:
                    os.remove(filename)
                except:
                    pass
                
                return {
                    'content': content,
                    'url': info.get('webpage_url', url),
                    'title': info.get('title', 'Instagram Story'),
                    'author': info.get('uploader', ''),
                    'is_video': is_video,
                    'ext': 'mp4' if is_video else 'jpg'
                }
                
            except Exception as e:
                error_msg = str(e)
                if "two-factor" in error_msg.lower():
                    raise Exception("2FA required - please use cookies file instead")
                elif "login" in error_msg.lower():
                    raise Exception("Login required - cookies may be expired. Please refresh your cookies.")
                elif "format" in error_msg.lower():
                    # Try a simpler format
                    try:
                        print("Trying with simpler format...")
                        ydl_opts['format'] = 'best'
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        with open(filename, 'rb') as f:
                            content = f.read()
                        os.remove(filename)
                        return {
                            'content': content,
                            'url': info.get('webpage_url', url),
                            'title': info.get('title', ''),
                            'author': info.get('uploader', ''),
                            'is_video': True,
                            'ext': info.get('ext', 'mp4')
                        }
                    except:
                        raise Exception(f"yt-dlp failed: {error_msg}")
                else:
                    raise Exception(f"yt-dlp failed: {error_msg}")