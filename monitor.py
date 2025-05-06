from monitors.price_checker import run_price_monitor
from config.constants import ITEM_NAMES
from dotenv import load_dotenv
from utils.item_expander import expand_item_variants

load_dotenv()

def main():
    itens_expandidos = expand_item_variants(ITEM_NAMES)
    run_price_monitor(itens_expandidos)  # Executa análise e envia os alertas

if __name__ == "__main__":
    main()