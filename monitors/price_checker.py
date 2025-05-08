import logging
from typing import List, Dict
from services.albion_api import get_item_prices, get_item_history
from notifications.alert_runner import run_alerts
from utils.filters import filter_best_offers

logger = logging.getLogger(__name__)

def fetch_market_data(item_variants: List[Dict]) -> List[Dict]:
    """
    Fetches current market prices for a list of item variants.

    Args:
        item_variants (List[Dict]): List of dictionaries containing "item_id" and optional "quality".

    Returns:
        List[Dict]: Filtered list of price data for the requested item variants.
    """
    item_ids = list({item["item_id"] for item in item_variants})
    logger.info(f"Fetching prices for {len(item_ids)} items in batch...")

    all_prices = get_item_prices(item_ids)

    filtered_prices = []
    for item in item_variants:
        item_id = item["item_id"]
        quality = item.get("quality")
        matched = [
            entry for entry in all_prices
            if entry["item_id"] == item_id and (quality is None or entry.get("quality") == quality)
        ]
        filtered_prices.extend(matched)

    return filtered_prices

def fetch_all_history(item_variants: List[Dict], days: int = 7) -> Dict[str, Dict]:
    """
    Fetches daily historical price data for all variants of each item.

    Args:
        item_variants (List[Dict]): List of dictionaries with "item_id" and optional "quality".
        days (int): Number of days of historical data to retrieve.

    Returns:
        Dict[str, Dict]: Dictionary of historical data grouped by item@city.
    """
    item_ids = list({item["item_id"] for item in item_variants})
    logger.info(f"Fetching historical price data for {len(item_ids)} items in batch...")

    raw_data = get_item_history(item_ids, days)
    history_data: Dict[str, Dict] = {}
    quality_map = {item["item_id"]: item.get("quality", 1) for item in item_variants}

    for entry in raw_data:
        item_id = entry.get("item_id")
        city = entry.get("location")
        quality = entry.get("quality", 1)

        if not item_id or not city:
            continue

        expected_quality = quality_map.get(item_id)
        if expected_quality is not None and expected_quality != quality:
            continue

        key = f"{item_id}@{city}"
        history_data[key] = {
            "item_id": item_id,
            "city": city,
            "quality": quality,
            "data": [entry]
        }

    return history_data

def run_price_monitor(item_variants: List[Dict]) -> None:
    """
    Runs the full price monitoring routine:
    - Fetches market data
    - Filters best offers
    - Fetches historical data
    - Triggers alerts

    Args:
        item_variants (List[Dict]): List of item variant definitions to monitor.
    """
    logger.info("🔄 Fetching current market data...")
    market_data = fetch_market_data(item_variants)

    logger.info("✅ Filtering best offers...")
    filtered_data = filter_best_offers(market_data)

    logger.info("📈 Fetching historical price data...")
    history = fetch_all_history(item_variants)

    logger.info("🚨 Triggering alert system...")
    run_alerts(filtered_data, item_variants, history=history)