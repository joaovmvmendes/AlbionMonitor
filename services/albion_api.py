import requests
import time
import logging
from typing import List, Dict, Optional
from config.constants import CITIES

logger = logging.getLogger(__name__)

API_BASE_PRICE = "https://west.albion-online-data.com/api/v2/stats/prices"
API_BASE_HISTORY = "https://west.albion-online-data.com/api/v2/stats/history"
API_BASE_CHARTS = "https://west.albion-online-data.com/api/v2/stats/charts"

_price_cache = {}

def get_item_prices(item_id: str, quality: Optional[int] = None) -> List[Dict]:
    """
    Fetches item prices across all configured cities from the Albion API.

    Parameters:
        item_id (str): The unique identifier of the item.
        quality (Optional[int]): Quality level of the item (1 to 5).

    Returns:
        List[Dict]: List of price entries or empty list on error.
    """
    key = f"{item_id}|{quality or 'any'}"
    if key in _price_cache:
        return _price_cache[key]

    logger.info(f"Fetching prices for: {item_id}" + (f" (Quality {quality})" if quality else ""))
    params = {"locations": ",".join(CITIES)}
    if quality:
        params["qualities"] = quality

    try:
        response = requests.get(f"{API_BASE_PRICE}/{item_id}.json", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        _price_cache[key] = data
        time.sleep(0.35)  # prevent API rate limiting
        return data
    except Exception as e:
        logger.warning(f"Failed to fetch prices for {item_id}: {e}")
        return []


def get_item_history(item_id: str, city: str, days: int = 7) -> List[Dict]:
    """
    Fetches historical daily prices for an item in a specific city.

    Parameters:
        item_id (str): Item identifier.
        city (str): City name.
        days (int): Number of days to retrieve.

    Returns:
        List[Dict]: Historical data.
    """
    url = f"{API_BASE_HISTORY}/{item_id}.json"
    params = {
        "locations": city,
        "time-scale": 24,
        "qualities": "1,2,3,4,5"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()[:days]
    except requests.RequestException as e:
        logger.warning(f"Error fetching price history for {item_id}@{city}: {e}")
        return []

def get_item_chart(item_id: str, city: str, quality: int = 1, days: int = 3) -> List[Dict]:
    """
    Fetches hourly average prices to build charts.

    Parameters:
        item_id (str): Item identifier.
        city (str): City name.
        quality (int): Quality level (default: 1).
        days (int): Number of days to retrieve.

    Returns:
        List[Dict]: List of {timestamp, avg_price} for plotting.
    """
    base_name = item_id.split("@")[0]
    url = f"{API_BASE_CHARTS}/{base_name}"
    params = {
        "locations": city,
        "qualities": quality,
        "time-scale": 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        result = response.json()

        for entry in result:
            if entry.get("location") == city and entry.get("quality") == quality:
                timestamps = entry["data"]["timestamps"]
                prices = entry["data"]["prices_avg"]

                if len(timestamps) != len(prices):
                    logger.warning(f"Inconsistent chart data for {base_name}@{city}")
                    return []

                return [
                    {"timestamp": ts, "avg_price": price}
                    for ts, price in zip(timestamps[-24 * days:], prices[-24 * days:])
                ]
    except requests.RequestException as e:
        logger.warning(f"Error fetching chart data for {base_name}@{city}: {e}")

    return []