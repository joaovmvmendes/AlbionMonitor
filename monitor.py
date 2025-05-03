from monitors.price_checker import run_price_monitor
from alerts.telegram import send_telegram_message
from config.constants import ITEM_NAMES
from dotenv import load_dotenv
from utils.item_expander import expand_item_variants

load_dotenv()

def main():
    itens_expandidos = expand_item_variants(ITEM_NAMES)
    mensagens_arb = run_price_monitor(itens_expandidos)
    mensagem_final = "\n\n".join(mensagens_arb)

    print("\n[PREVIEW] Mensagem final que será enviada:\n")
    print(mensagem_final)

    send_telegram_message(mensagem_final)

if __name__ == "__main__":
    main()
