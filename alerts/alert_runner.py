import os
from data.data_process import analisar_arbitragem, agrupar_por, analisar_tendencia_historica
from alerts.message_builder import format_arbitragem_alert, format_trend_alerts
from alerts.telegram import send_telegram_message, send_telegram_photo

MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.15))
MAX_PROFIT_MARGIN = float(os.getenv("MAX_PROFIT_MARGIN", 10))

def run_alerts(data, item_names, agrupamento=None, historico=None):
    # 🔥 ARBITRAGEM
    oportunidades = analisar_arbitragem(data, item_names, MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN)
    alertas = format_arbitragem_alert(oportunidades)

    for texto, imagem in alertas:
        send_telegram_message(texto)
        if imagem:
            if send_telegram_photo(imagem):
                if os.path.exists(imagem):
                    try:
                        os.remove(imagem)  # remove só se ainda existir
                    except Exception as e:
                        print(f"⚠️ Erro ao tentar remover a imagem: {e}")

    # 📈 TENDÊNCIAS DE PREÇO
    for msg in format_trend_alerts(historico, analisar_tendencia_historica, MIN_PROFIT_MARGIN):
        send_telegram_message(msg)