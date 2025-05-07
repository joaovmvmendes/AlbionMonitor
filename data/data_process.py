import logging
from collections import defaultdict
from typing import List, Dict, Optional, Any

from services.albion_api import get_item_history

logger = logging.getLogger(__name__)


def analyze_arbitrage(
    data: List[Dict],
    item_variants: List[Dict],
    min_margin: float = 0.15,
    max_margin: float = 1.0
) -> List[Dict]:
    """
    Identifies arbitrage opportunities based on item prices across cities.

    Parameters:
        data (List[Dict]): Market entries from the API.
        item_variants (List[Dict]): List of item variants with item_id and quality.
        min_margin (float): Minimum profit margin to consider.
        max_margin (float): Maximum profit margin to avoid anomalies.

    Returns:
        List[Dict]: Sorted list of profitable opportunities.
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
    Groups market data by city or item.

    Parameters:
        data (List[Dict]): Market entries.
        item_names (List[str]): Valid item_ids to include.
        group_key (str): 'city' or 'item'.

    Returns:
        Dict[str, List[Dict]]: Grouped values by city or item_id.
    """
    grouped = defaultdict(list)

    if group_key not in ("city", "item"):
        return grouped

    for item in data:
        item_id = item.get("item_id")
        city = item.get("city", "Unknown")
        sell_price_min = item.get("sell_price_min", 0)
        sell_price_max = item.get("sell_price_max", 0)

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
    Analyzes price trends over time and identifies significant variations.

    Parameters:
        item_histories (Dict[str, List[Dict]]): Historical price data.
        min_variation (float): Minimum variation to trigger an alert.

    Returns:
        List[Dict]: Sorted list of alerts with strong price movement.
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
    days: int = 7
) -> Optional[int]:
    """
    Calculates the average number of items sold per day over a period.

    Parameters:
        item_id (str): Item identifier.
        city (str): City name.
        quality (int): Quality level.
        days (int): Number of days to consider.

    Returns:
        Optional[int]: Average items sold per day or None if unavailable.
    """
    history = get_item_history(item_id, city, days)
    if not history:
        logger.debug(f"No history for {item_id} in {city} (quality {quality})")
        return None

    counts = []
    for entry in history:
        if entry.get("quality") != quality:
            continue

        daily_data = entry.get("data", [])[:days]
        counts.extend(
            d.get("item_count", 0) for d in daily_data if d.get("item_count", 0) > 0
        )

    if not counts:
        logger.debug(f"No valid sales counts for {item_id} in {city} (quality {quality})")
        return None

    return sum(counts) // len(counts)