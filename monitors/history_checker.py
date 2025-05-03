from data.state_manager import load_last_state, save_current_state
from data.data_process import analisar_tendencia_historica
from alerts.message_builder import format_trend_alerts
from alerts.telegram import send_telegram_message
from config.settings import MIN_PROFIT_MARGIN

def run_history_monitor():
    historico = load_last_state()
    mensagens = format_trend_alerts(historico, analisar_tendencia_historica, MIN_PROFIT_MARGIN)

    if mensagens:
        texto_final = "\n\n".join(mensagens)
        send_telegram_message(texto_final)

    save_current_state(historico)
