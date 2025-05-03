from monitors.price_checker import run_price_monitor
from monitors.history_checker import run_history_monitor
from config.constants import ITEMS_MONITORADOS
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    item_names = ITEMS_MONITORADOS
    run_price_monitor(item_names)
    run_history_monitor()

if __name__ == "__main__":
    main()
