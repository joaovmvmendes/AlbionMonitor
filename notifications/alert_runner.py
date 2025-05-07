import logging
from typing import List, Dict, Optional

from data.data_process import (
    analyze_arbitrage,
    group_by,
    analyze_historical_trend
)
from notifications.message_builder import (
    format_arbitrage_alerts,
    format_trend_alerts
)
from notifications.telegram import send_telegram_message
from utils.media import send_image_and_cleanup
from config.settings import MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN

logger = logging.getLogger(__name__)

def run_alerts(
    data: List[Dict],
    item_variants: List[Dict],
    group_by_key: Optional[str] = None,
    history: Optional[Dict] = None
) -> None:
    """
    Executes alert logic for arbitrage opportunities and price trends.

    Parameters:
        data (List[Dict]): Filtered market data entries.
        item_variants (List[Dict]): List of item variants with IDs and quality.
        group_by_key (Optional[str]): Not used in current version (reserved for future).
        history (Optional[Dict]): Historical market data for trend analysis.
    """
    logger.info("🔔 Starting arbitrage alert analysis...")
    try:
        opportunities = analyze_arbitrage(data, item_variants, MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN)
        alerts = format_arbitrage_alerts(opportunities)

        for text, image_path in alerts:
            send_telegram_message(text)
            if image_path:
                send_image_and_cleanup(image_path)

        logger.info(f"✅ {len(alerts)} arbitrage alerts sent.")
    except Exception as e:
        logger.exception(f"Error during arbitrage alert execution: {e}")

    logger.info("📉 Starting price trend alert analysis...")
    try:
        trend_alerts = format_trend_alerts(history or {}, analyze_historical_trend, MIN_PROFIT_MARGIN)

        for msg in trend_alerts:
            send_telegram_message(msg)

        logger.info(f"✅ {len(trend_alerts)} trend alerts sent.")
    except Exception as e:
        logger.exception(f"Error during trend alert execution: {e}")