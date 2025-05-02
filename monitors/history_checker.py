from data.state_manager import load_last_state, save_current_state
from data.data_process import analisar_tendencia_historica
from alerts.message_builder import format_trend_alerts
from alerts.telegram import send_telegram_message
import os

MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.15))

def run_history_monitor():
    historico = load_last_state()
    mensagens = format_trend_alerts(historico, analisar_tendencia_historica, MIN_PROFIT_MARGIN)
    for msg in mensagens:
        send_telegram_message(msg)
    save_current_state(historico)
