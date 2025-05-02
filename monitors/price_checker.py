from data_fetch.api_prices import get_item_prices_from_api
from data.data_process import analisar_arbitragem
from alerts.message_builder import format_arbitragem_alert
from alerts.telegram import send_telegram_message
import os

MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.15))
MAX_PROFIT_MARGIN = float(os.getenv("MAX_PROFIT_MARGIN", 10))

def run_price_monitor(item_names, qualidade=None):
    for item in item_names:
        data = get_item_prices_from_api(item, qualidade)
        oportunidades = analisar_arbitragem(data, [item], MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN)
        mensagens = format_arbitragem_alert(oportunidades)
        for msg in mensagens:
            send_telegram_message(msg)
