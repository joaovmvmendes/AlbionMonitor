# config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file (only used in local development)
if os.path.exists(".env"):
    load_dotenv()

# Profit margin thresholds used for item filtering
MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.15))  # Minimum profit considered viable (default: 15%)
MAX_PROFIT_MARGIN = float(os.getenv("MAX_PROFIT_MARGIN", 10.0))  # Maximum profit cap to avoid anomalies (default: 1000%)

# Telegram bot configuration for sending alerts
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")       # Required
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")   # Required

# Path to the local file that stores the last known state (e.g., previously alerted items)
STATE_FILE_PATH = "last_state.json"