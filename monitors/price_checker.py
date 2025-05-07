import logging
from typing import List, Dict
from services.albion_api import get_item_prices, get_item_history
from notifications.alert_runner import run_alerts
from config.constants import CITIES
from utils.filters import filter_best_offers

logger = logging.getLogger(__name__)

def fetch_market_data(item_variants: List[Dict]) -> List[Dict]:
    """
    Fetches market prices for all item variants.

    Parameters:
        item_variants (List[Dict]): List of items with item_id and quality.

    Returns:
        List[Dict]: Combined market data.
    """
    all_data = []
    for item in item_variants:
        item_id = item["item_id"]
        quality = item.get("quality")
        logger.info(f"Fetching prices for: {item_id}" + (f" (Quality {quality})" if quality else ""))
        data = get_item_prices(item_id, quality)
        all_data.extend(data)
    return all_data

def fetch_all_history(item_variants: List[Dict], days: int = 7) -> Dict[str, Dict]:
    """
    Fetches historical pricing data for each item variant in every configured city.

    Parameters:
        item_variants (List[Dict]): List of items with item_id and quality.
        days (int): Number of days to retrieve history for.

    Returns:
        Dict[str, Dict]: History grouped by item@city.
    """
    history = {}
    for item in item_variants:
        item_id = item["item_id"]
        quality = item.get("quality", 1)

        for city in CITIES:
            key = f"{item_id}@{city}"
            logger.info(f"Fetching price history: {key} (Quality {quality})")
            data = get_item_history(item_id, city, days)
            history[key] = {
                "item_id": item_id,
                "city": city,
                "quality": quality,
                "data": data
            }

    return history

def run_price_monitor(item_variants: List[Dict]) -> None:
    """
    Runs the main market monitoring logic:
    - Fetch prices
    - Filter best offers
    - Fetch history
    - Trigger alerts
    """
    logger.info("🔄 Fetching current market data...")
    market_data = fetch_market_data(item_variants)

    logger.info("✅ Filtering best offers...")
    filtered_data = filter_best_offers(market_data)

    logger.info("📈 Fetching sales history...")
    history = fetch_all_history(item_variants)

    logger.info("🚨 Running alert logic...")
    run_alerts(filtered_data, item_variants, history=history)