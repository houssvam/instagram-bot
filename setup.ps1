#!/usr/bin/env pwsh
Write-Host "🚀 Setting up Instagram Ultimate Bot..." -ForegroundColor Green

# Git initialization
git init
git branch -M main

# Create .gitignore
@"
__pycache__/
*.py[cod]
*$py.class
.env
.venv
venv/
env/
dist/
build/
*.egg-info/
.DS_Store
logs/
*.log
*.db
*.sqlite3
.cache/
.pytest_cache/
.coverage
htmlcov/
.idea/
.vscode/
*.swp
*.swo
*~
"@ | Out-File -FilePath .gitignore -Encoding UTF8

# Create README
@"
# 🤖 Instagram Ultimate Bot

The most advanced Telegram bot for Instagram content downloading

## 🚀 Features
- Mesh network processing
- Quantum-safe encryption
- ML-based predictive caching
- Multi-strategy extraction
- Terminal-first development
"@ | Out-File -FilePath README.md -Encoding UTF8

# Create requirements.txt
@"
# Core
aiohttp>=3.9.0
asyncio>=3.4.3
python-telegram-bot>=20.6

# Download engines
yt-dlp>=2023.12.30
instaloader>=4.10

# Terminal UI
rich>=13.7.0
prompt-toolkit>=3.0.43

# Security
cryptography>=41.0.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
"@ | Out-File -FilePath requirements.txt -Encoding UTF8

# Create .env file with your credentials
$encryptionKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
$jwtSecret = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
$nodeId = [guid]::NewGuid().ToString()

@"
# Telegram
TELEGRAM_BOT_TOKEN=8512072570:AAG4yjjxzEkmk7QM6q1KwqfKpcMiRFijW14

# Instagram
INSTAGRAM_USERNAME=kyrovinalvlad
INSTAGRAM_PASSWORD=asxzsdcx

# Database
REDIS_URL=redis://localhost:6379
MONGODB_URL=mongodb://localhost:27017

# Security
ENCRYPTION_KEY=$encryptionKey
JWT_SECRET=$jwtSecret

# Network
NODE_ID=$nodeId
"@ | Out-File -FilePath .env -Encoding UTF8

Write-Host "✅ Setup complete! Run: python -m venv .venv" -ForegroundColor Green
