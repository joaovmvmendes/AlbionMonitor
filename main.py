import logging
import sys
from dotenv import load_dotenv

from monitors.price_checker import run_price_monitor
from config.constants import ITEM_NAMES
from utils.item_expander import expand_item_variants

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("🔄 Expanding configured items...")
    expanded_items = expand_item_variants(ITEM_NAMES)
    run_price_monitor(expanded_items)

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        logger.exception(f"Fatal error occurred: {error}")
        sys.exit(1)