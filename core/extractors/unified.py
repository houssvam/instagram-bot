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
        
        # Determine content type
        content_type = 'unknown'
        if data.get('is_video', False):
            content_type = 'video'
        elif data.get('is_image', False):
            content_type = 'photo'
        else:
            # Try to detect from data
            if isinstance(data.get('content'), bytes):
                # Check first few bytes for image signatures
                if len(data['content']) > 2 and data['content'][:2] == b'\xff\xd8':  # JPEG
                    content_type = 'photo'
                elif len(data['content']) > 4 and data['content'][:4] == b'\x89PNG':  # PNG
                    content_type = 'photo'
                elif len(data['content']) > 4 and data['content'][:4] == b'GIF8':  # GIF
                    content_type = 'photo'
                else:
                    content_type = 'video'  # Assume video
        
        return {
            'type': content_type,
            'data': data['content'],
            'caption': data.get('caption', '') or data.get('title', ''),
            'metadata': {
                'url': data.get('url', ''),
                'author': data.get('author', ''),
                'timestamp': data.get('timestamp', ''),
                'strategy': raw_result['strategy']
            }
        }

class YTDLPStrategy:
    async def download(self, url: str) -> Dict:
        """Download using yt-dlp with cookies - supports reels, posts, images, and carousels"""
        
        # Check for cookies file
        cookies_file = None
        if os.path.exists('instagram_cookies.txt'):
            cookies_file = 'instagram_cookies.txt'
            print(f"Using cookies from {cookies_file}")
        elif os.path.exists('cookies/instagram_cookies.txt'):
            cookies_file = 'cookies/instagram_cookies.txt'
            print(f"Using cookies from {cookies_file}")
        
        # Detect content type
        is_story = '/stories/' in url
        is_post = '/p/' in url or '/reel/' in url
        
        # Base options
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'outtmpl': 'temp/%(id)s.%(ext)s',
        }
        
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
                # First extract info without downloading to check what it is
                info = ydl.extract_info(url, download=False)
                
                # Check if it's a playlist (carousel)
                if 'entries' in info:
                    entries_count = len(info['entries'])
                    print(f"Found carousel/post with {entries_count} items")
                    
                    if entries_count == 0:
                        # This might be a single image - try downloading directly
                        print("No items found, trying direct download...")
                        info = ydl.extract_info(url, download=True)
                    else:
                        # Download the first item
                        first_entry = info['entries'][0]
                        if 'url' in first_entry:
                            item_url = first_entry['url']
                        else:
                            # Try to get the URL from the entry
                            item_url = first_entry.get('webpage_url', url)
                        info = ydl.extract_info(item_url, download=True)
                else:
                    # Single item - download directly
                    info = ydl.extract_info(url, download=True)
                
                # Get file path
                filename = ydl.prepare_filename(info)
                
                # Check if file exists
                if not os.path.exists(filename):
                    # Try to find any file in temp
                    for file in os.listdir('temp'):
                        if file.endswith(('.mp4', '.mkv', '.webm', '.jpg', '.jpeg', '.png', '.gif')):
                            filename = os.path.join('temp', file)
                            break
                
                # Read file
                with open(filename, 'rb') as f:
                    content = f.read()
                
                # Determine content type
                is_video = filename.endswith(('.mp4', '.mkv', '.webm'))
                is_image = filename.endswith(('.jpg', '.jpeg', '.png', '.gif'))
                
                # Clean up
                try:
                    os.remove(filename)
                except:
                    pass
                
                # Get caption if available
                caption = info.get('title', '')
                if info.get('description'):
                    caption = info.get('description')
                
                return {
                    'content': content,
                    'url': info.get('webpage_url', url),
                    'title': caption or 'Instagram content',
                    'author': info.get('uploader', info.get('channel', '')),
                    'is_video': is_video,
                    'is_image': is_image,
                    'ext': 'mp4' if is_video else 'jpg'
                }
                
            except Exception as e:
                error_msg = str(e)
                if "two-factor" in error_msg.lower():
                    raise Exception("2FA required - please use cookies file instead")
                elif "login" in error_msg.lower() or "log in" in error_msg.lower():
                    if is_story:
                        raise Exception("This story requires login. Make sure you follow this account and the story is still active.")
                    else:
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
                        is_video = filename.endswith(('.mp4', '.mkv', '.webm'))
                        return {
                            'content': content,
                            'url': info.get('webpage_url', url),
                            'title': info.get('title', ''),
                            'author': info.get('uploader', ''),
                            'is_video': is_video,
                            'is_image': not is_video,
                            'ext': 'mp4' if is_video else 'jpg'
                        }
                    except:
                        raise Exception(f"Download failed: {error_msg}")
                else:
                    raise Exception(f"Download failed: {error_msg}")