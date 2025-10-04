"""
Foxcode Shorter - Telegram Bot
Main bot application with all handlers
Created by: codewithkanchan.com
"""

import logging
import json
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
import aiohttp
import sys

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Import bot modules
from handlers import (
    start_handler, help_handler, shorten_handler, manage_handler,
    wallet_handler, support_handler, callback_handler, url_handler,
    terms_handler, stats_handler
)
from keyboards import get_main_keyboard, get_terms_keyboard
from wallet import WalletManager
from admin import AdminManager

class FoxcodeShorterBot:
    def __init__(self, token: str, api_base_url: str):
        self.token = token
        self.api_base_url = api_base_url
        self.application = Application.builder().token(token).build()
        self.wallet_manager = WalletManager(api_base_url)
        self.admin_manager = AdminManager(api_base_url)
        self.setup_handlers()

    def setup_handlers(self):
        """Setup all bot handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", start_handler))
        self.application.add_handler(CommandHandler("help", help_handler))
        self.application.add_handler(CommandHandler("shorten", shorten_handler))
        self.application.add_handler(CommandHandler("manage", manage_handler))
        self.application.add_handler(CommandHandler("wallet", wallet_handler))
        self.application.add_handler(CommandHandler("support", support_handler))
        self.application.add_handler(CommandHandler("terms", terms_handler))
        self.application.add_handler(CommandHandler("stats", stats_handler))

        # Callback query handler for inline keyboards
        self.application.add_handler(CallbackQueryHandler(callback_handler))

        # URL message handler
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, url_handler
        ))

        # Error handler
        self.application.add_error_handler(self.error_handler)

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle errors"""
        logger.error(msg="Exception while handling an update:", exc_info=context.error)

        if update and hasattr(update, 'effective_message'):
            await update.effective_message.reply_text(
                "âŒ An error occurred. Please try again later or contact support."
            )

    def run(self):
        """Run the bot"""
        logger.info("ðŸ¤– Starting Foxcode Shorter Bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

# Load configuration
try:
    with open('../backend/config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    logger.error("âŒ config.json not found!")
    sys.exit(1)

if __name__ == '__main__':
    BOT_TOKEN = os.getenv('BOT_TOKEN', config['bot_token'])
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("âŒ Please set your BOT_TOKEN in config.json or environment variables")
        sys.exit(1)

    bot = FoxcodeShorterBot(BOT_TOKEN, API_BASE_URL)
    bot.run()
