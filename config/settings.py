# 📁 config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables from .env (only in local environments)
if os.path.exists(".env"):
    load_dotenv()

# ⬆️ Profit margin thresholds for arbitrage filtering
MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.15))
MAX_PROFIT_MARGIN = float(os.getenv("MAX_PROFIT_MARGIN", 10))

# 📢 Telegram bot configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 📂 Local file to store bot state
STATE_FILE_PATH = "last_state.json"