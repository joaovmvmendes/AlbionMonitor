import requests
import time
import logging
from typing import List, Dict, Union

logger = logging.getLogger(__name__)

API_BASE_PRICE = "https://west.albion-online-data.com/api/v2/stats/prices"
API_BASE_HISTORY = "https://west.albion-online-data.com/api/v2/stats/history"
API_BASE_CHARTS = "https://west.albion-online-data.com/api/v2/stats/charts"

_price_cache: Dict[str, List[Dict]] = {}

def get_item_prices(item_ids: Union[str, List[str]]) -> List[Dict]:
    """
    Fetches current prices for one or more items across all cities and qualities.

    Args:
        item_ids (Union[str, List[str]]): Single item ID or list of item IDs.

    Returns:
        List[Dict]: List of price data for all available cities and qualities.
    """
    if isinstance(item_ids, str):
        item_ids = [item_ids]

    key = ",".join(sorted(item_ids))
    if key in _price_cache:
        return _price_cache[key]

    joined_ids = ",".join(item_ids)
    logger.info(f"Fetching prices for: {joined_ids}")
    try:
        response = requests.get(f"{API_BASE_PRICE}/{joined_ids}.json", timeout=10)
        response.raise_for_status()
        data = response.json()
        _price_cache[key] = data
        time.sleep(0.35)  # API rate limit protection
        return data
    except Exception as e:
        logger.warning(f"Failed to fetch prices for {joined_ids}: {e}")
        return []

def get_item_history(item_ids: Union[str, List[str]], days: int = 7) -> List[Dict]:
    """
    Fetches historical price data for multiple items across all cities and qualities.

    Args:
        item_ids (Union[str, List[str]]): Single or multiple item IDs.
        days (int): Number of days of history to retain per entry.

    Returns:
        List[Dict]: Combined list of historical price entries for each item.
    """
    if isinstance(item_ids, str):
        item_ids = [item_ids]

    joined_ids = ",".join(item_ids)
    url = f"{API_BASE_HISTORY}/{joined_ids}.json"
    params = {
        "time-scale": 24,
        "qualities": "1,2,3,4,5"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Limit number of entries inside each entry's 'data' field
        for entry in data:
            entry["data"] = entry.get("data", [])[:days]

        return data
    except requests.RequestException as e:
        logger.warning(f"Error fetching price history for {joined_ids}: {e}")
        return []