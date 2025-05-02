from monitors.price_checker import run_price_monitor
from monitors.history_checker import run_history_monitor
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    item_names = [
        "T4_BAG", "T5_BAG", "T6_BAG",
        "T4_CAPE", "T5_CAPE", "T6_CAPE"
    ]  # substitua pelos itens desejados

    run_price_monitor(item_names)
    run_history_monitor()

if __name__ == "__main__":
    main()
