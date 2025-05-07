import logging
import os
import sys
from dotenv import load_dotenv

from monitors.price_checker import run_price_monitor
from config.constants import ITEM_NAMES
from utils.item_expander import expand_item_variants

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# check for required environment variables and warn if missing
REQUIRED_ENV_VARS = ["TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID"]
for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        logger.warning(f"Missing required environment variable: {var}")

def main():
    """Main entry point of the AlbionMonitor application."""
    logger.info("🔍 Expanding configured items...")
    expanded_items = expand_item_variants(ITEM_NAMES)
    run_price_monitor(expanded_items)

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        logger.exception(f"Fatal error occurred: {error}")
        sys.exit(1)