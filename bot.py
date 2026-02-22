#!/usr/bin/env python3
"""
Instagram Ultimate Bot - Main Entry Point
"""

# Fix Windows encoding first
import fix_encoding

import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import os
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ContextTypes, CallbackQueryHandler
)
from core.extractors.unified import UnifiedExtractor
import config

# Setup logging - remove emojis for Windows compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class UltimateInstagramBot:
    """Main bot class"""
    
    def __init__(self):
        self.token = config.TELEGRAM_BOT_TOKEN
        self.extractor = UnifiedExtractor()
        self.stats = {
            'users': set(),
            'downloads': 0,
            'bytes_sent': 0,
            'errors': 0
        }
        
    async def initialize(self):
        """Initialize all components"""
        logger.info("Starting Instagram Ultimate Bot...")
        
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        os.makedirs('temp', exist_ok=True)
        os.makedirs('cookies', exist_ok=True)
        
        logger.info("Bot initialization complete")
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        self.stats['users'].add(user.id)
        
        welcome_text = f"""
Welcome to Ultimate Instagram Bot!

Hello {user.first_name}! I download Instagram content.

Features:
• Download Instagram posts, reels, stories
• Fast and reliable
• Multiple download strategies

Stats:
• Users served: {len(self.stats['users'])}
• Total downloads: {self.stats['downloads']}

Just send me any Instagram URL to start!
        """
        
        await update.message.reply_text(welcome_text)
        
    async def handle_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Instagram URLs"""
        url = update.message.text
        user = update.effective_user
        
        logger.info(f"Download request from {user.id}: {url}")
        
        # Send initial status
        status_msg = await update.message.reply_text("Processing your request...")
        
        try:
            # Extract content
            result = await self.extractor.extract(url)
            
            if not result['success']:
                error_msg = result.get('error', 'Unknown error')
                if "two-factor" in error_msg.lower():
                    await status_msg.edit_text(
                        "❌ Instagram requires two-factor authentication.\n"
                        "Please disable 2FA temporarily or use a different account without 2FA."
                    )
                else:
                    await status_msg.edit_text(f"❌ Failed: {error_msg}")
                return
            
            # Process result
            media = await self.extractor.process(result)
            
            await status_msg.edit_text("Sending to Telegram...")
            
            # Send to user
            if media['type'] == 'video':
                await update.message.reply_video(
                    video=media['data'],
                    caption=media.get('caption', '')[:200]  # Telegram caption limit
                )
            else:
                await update.message.reply_photo(
                    photo=media['data'],
                    caption=media.get('caption', '')[:200]
                )
            
            # Update stats
            self.stats['downloads'] += 1
            self.stats['bytes_sent'] += len(media['data'])
            
            await status_msg.delete()
            await update.message.reply_text("Download complete!")
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            self.stats['errors'] += 1
            await status_msg.edit_text(f"❌ Failed to download: {str(e)[:100]}")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
    def run(self):
        """Run the bot"""
        # Check token
        if not self.token or self.token == 'your_token_here':
            logger.error("Please set TELEGRAM_BOT_TOKEN in .env file")
            return
        
        # Create application
        app = Application.builder().token(self.token).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            self.handle_url
        ))
        
        # Add error handler
        app.add_error_handler(self.error_handler)
        
        # Initialize components
        asyncio.get_event_loop().run_until_complete(self.initialize())
        
        # Start bot
        logger.info("Bot is running... Press Ctrl+C to stop")
        app.run_polling()

if __name__ == "__main__":
    bot = UltimateInstagramBot()
    bot.run()
