import logging
from collections import defaultdict
from typing import List, Dict, Optional

from services.albion_api import get_item_history

logger = logging.getLogger(__name__)


def analyze_arbitrage(
    data: List[Dict],
    item_variants: List[Dict],
    min_margin: float = 0.15,
    max_margin: float = 1.0
) -> List[Dict]:
    """
    Identifies arbitrage opportunities based on item price differences across cities.

    Args:
        data (List[Dict]): Current market data entries.
        item_variants (List[Dict]): List of item variants with 'item_id' and 'quality'.
        min_margin (float): Minimum acceptable profit margin.
        max_margin (float): Maximum acceptable profit margin to exclude outliers.

    Returns:
        List[Dict]: Sorted list of arbitrage opportunities.
    """
    opportunities = []

    for variant in item_variants:
        item_id = variant["item_id"]
        quality = variant.get("quality", 1)

        offers = [
            entry for entry in data
            if entry.get("item_id") == item_id
            and entry.get("sell_price_min", 0) > 0
            and entry.get("quality") == quality
        ]

        if len(offers) < 2:
            logger.debug(f"Not enough offers for {item_id} (quality {quality}) — skipping.")
            continue

        offers.sort(key=lambda x: x["sell_price_min"])
        origin = offers[0]
        destination = offers[-1]

        origin_price = origin["sell_price_min"]
        destination_price = destination["sell_price_min"]
        profit = destination_price - origin_price
        profit_margin = profit / origin_price

        if min_margin <= profit_margin < max_margin:
            opportunities.append({
                "item": item_id,
                "origin": origin["city"],
                "destination": destination["city"],
                "origin_price": origin_price,
                "destination_price": destination_price,
                "profit": profit,
                "margin": profit_margin,
                "quality": quality
            })

    opportunities.sort(key=lambda x: x["margin"], reverse=True)
    return opportunities


def group_by(
    data: List[Dict],
    item_names: List[str],
    group_key: str
) -> Dict[str, List[Dict]]:
    """
    Groups market data entries by city or item.

    Args:
        data (List[Dict]): Market data entries.
        item_names (List[str]): Valid item_ids to include.
        group_key (str): Key to group by ('city' or 'item').

    Returns:
        Dict[str, List[Dict]]: Grouped data dictionary.
    """
    grouped = defaultdict(list)

    if group_key not in ("city", "item"):
        return grouped

    for entry in data:
        item_id = entry.get("item_id")
        city = entry.get("city", "Unknown")
        sell_price_min = entry.get("sell_price_min", 0)
        sell_price_max = entry.get("sell_price_max", 0)

        if item_id in item_names and sell_price_min >= 0:
            key = city.upper() if group_key == "city" else item_id.upper()
            grouped[key].append({
                "min": sell_price_min,
                "max": sell_price_max,
                "item": item_id
            })

    return grouped


def analyze_historical_trend(
    item_histories: Dict[str, List[Dict]],
    min_variation: float = 0.10
) -> List[Dict]:
    """
    Identifies items with strong price variation over time.

    Args:
        item_histories (Dict[str, List[Dict]]): Historical data grouped by item@city.
        min_variation (float): Minimum required variation.

    Returns:
        List[Dict]: Sorted list of detected price variation alerts.
    """
    alerts = []

    for key, history in item_histories.items():
        parts = key.split("@")
        if len(parts) < 2:
            logger.warning(f"Invalid history key: {key}")
            continue

        item = "@".join(parts[:-1])
        city = parts[-1]

        if not history or "data" not in history[0]:
            continue

        history_info = history[0]["data"]
        if len(history_info) < 2:
            continue

        start_price = history_info[-1].get("prices_avg", 0)
        end_price = history_info[0].get("prices_avg", 0)

        if start_price == 0 or end_price == 0:
            continue

        variation = (end_price - start_price) / start_price

        if abs(variation) >= min_variation:
            alerts.append({
                "item": item,
                "city": city,
                "start_price": start_price,
                "end_price": end_price,
                "variation": variation
            })

    alerts.sort(key=lambda x: abs(x["variation"]), reverse=True)
    return alerts


def calculate_sales_average(
    item_id: str,
    city: str,
    quality: int = 1,
    days: int = 7,
    history_cache: Optional[List[Dict]] = None
) -> Optional[int]:
    """
    Computes the average number of items sold per day for a given item variant.

    Args:
        item_id (str): Unique name of the item.
        city (str): Target city.
        quality (int): Desired quality level.
        days (int): Number of days to average over.
        history_cache (Optional[List[Dict]]): Pre-fetched historical data to avoid API calls.

    Returns:
        Optional[int]: Average daily sales count or None if unavailable.
    """
    if history_cache is None:
        history_cache = get_item_history(item_id, days)

    filtered = [
        entry for entry in history_cache
        if entry.get("location") == city and entry.get("quality") == quality
    ]

    if not filtered:
        logger.debug(f"No historical data for {item_id} in {city} (quality {quality})")
        return None

    counts = []
    for entry in filtered:
        daily_data = entry.get("data", [])[:days]
        counts.extend(
            d.get("item_count", 0) for d in daily_data if d.get("item_count", 0) > 0
        )

    if not counts:
        logger.debug(f"No valid item counts for {item_id} in {city} (quality {quality})")
        return None

    return sum(counts) // len(counts)