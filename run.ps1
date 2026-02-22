#!/usr/bin/env pwsh

Write-Host "╔════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║   INSTAGRAM ULTIMATE BOT LAUNCHER ║" -ForegroundColor Blue
Write-Host "╚════════════════════════════════════╝" -ForegroundColor Blue

# Create logs directory
New-Item -ItemType Directory -Force -Path logs | Out-Null
New-Item -ItemType Directory -Force -Path temp | Out-Null

# Clear old logs
"" | Out-File -FilePath logs\bot.log

# Start the bot
Write-Host "🚀 Starting bot..." -ForegroundColor Green
Write-Host "📝 Logs being written to logs\bot.log" -ForegroundColor Yellow
Write-Host ""

# Run bot
python bot.py
