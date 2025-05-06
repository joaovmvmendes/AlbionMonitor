import os
from data.data_process import analyze_arbitrage, group_by, analyze_historical_trend
from notifications.message_builder import format_arbitrage_alerts, format_trend_alerts
from notifications.telegram import send_telegram_message, send_telegram_photo

MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.15))
MAX_PROFIT_MARGIN = float(os.getenv("MAX_PROFIT_MARGIN", 10))

def run_alerts(data, item_names, group_by_key=None, history=None):
    # 🔥 ARBITRAGE
    opportunities = analyze_arbitrage(data, item_names, MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN)
    alerts = format_arbitrage_alerts(opportunities)

    for text, image_path in alerts:
        send_telegram_message(text)  # message stays in Portuguese
        if image_path:
            if send_telegram_photo(image_path):
                if os.path.exists(image_path):
                    try:
                        os.remove(image_path)  # safely remove file if it exists
                    except Exception as e:
                        print(f"⚠️ Error trying to remove image: {e}")

    # 📈 PRICE TRENDS
    for msg in format_trend_alerts(history, analyze_historical_trend, MIN_PROFIT_MARGIN):
        send_telegram_message(msg)  # message stays in Portuguese