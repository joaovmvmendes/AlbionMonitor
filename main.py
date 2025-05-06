from monitors.price_checker import run_price_monitor
from config.constants import ITEM_NAMES
from dotenv import load_dotenv
from utils.item_expander import expand_item_variants

load_dotenv()

def main():
    expanded_items = expand_item_variants(ITEM_NAMES)
    run_price_monitor(expanded_items)  # Runs analysis and sends notifications

if __name__ == "__main__":
    main()