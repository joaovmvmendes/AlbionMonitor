import os
from data.data_process import analisar_arbitragem, agrupar_por, analisar_tendencia_historica
from alerts.message_builder import (
    format_arbitragem_alert,
    format_price_range_alerts,
    format_trend_alerts
)
from alerts.telegram import send_telegram_message

MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.15))
MAX_PROFIT_MARGIN = float(os.getenv("MAX_PROFIT_MARGIN", 10))

def run_alerts(data, item_names, agrupamento=None, historico=None):
    mensagens = []

    oportunidades = analisar_arbitragem(data, item_names, MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN)
    mensagens += format_arbitragem_alert(oportunidades)

    mensagens += format_price_range_alerts(data, item_names, agrupamento, agrupar_por)

    mensagens += format_trend_alerts(historico, analisar_tendencia_historica, MIN_PROFIT_MARGIN)

    for msg in mensagens:
        send_telegram_message(msg)
