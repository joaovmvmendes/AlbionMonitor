import os
from data.data_process import analyze_arbitrage, group_by, analyze_historical_trend
from notifications.message_builder import format_arbitrage_alerts, format_trend_alerts
from notifications.telegram import send_telegram_message
from utils.media import send_image_and_cleanup

from config.settings import MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN

def run_alerts(data, item_names, group_by_key=None, history=None):
    # 🔥 Arbitrage
    opportunities = analyze_arbitrage(data, item_names, MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN)
    alerts = format_arbitrage_alerts(opportunities)

    for text, image_path in alerts:
        send_telegram_message(text)
        if image_path:
            send_image_and_cleanup(image_path)

    # 📈 Price trends
    for msg in format_trend_alerts(history, analyze_historical_trend, MIN_PROFIT_MARGIN):
        send_telegram_message(msg)