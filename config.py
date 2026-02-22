import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# Instagram (optional for higher limits)
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME', '')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD', '')

# Database
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')

# Security
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', '')
JWT_SECRET = os.getenv('JWT_SECRET', '')

# Network
NODE_ID = os.getenv('NODE_ID', '')

# Paths
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / 'logs'
CACHE_DIR = BASE_DIR / 'cache'
TEMP_DIR = BASE_DIR / 'temp'

# Create directories
for dir_path in [LOGS_DIR, CACHE_DIR, TEMP_DIR]:
    dir_path.mkdir(exist_ok=True)

# Bot settings
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB (Telegram limit)
SUPPORTED_DOMAINS = [
    'instagram.com',
    'instagr.am',
    'reels'
]
