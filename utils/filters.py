from typing import List, Dict

def filter_best_offers(data: List[Dict]) -> List[Dict]:
    """
    Filters market data to keep only the lowest sell offer for each combination
    of item ID, quality level, and city.

    Parameters:
        data (List[Dict]): List of market entries from the API.

    Returns:
        List[Dict]: Filtered list with only the best offers per unique item-quality-city key.
    """
    best_by_key = {}

    for entry in data:
        item_id = entry.get("item_id")
        quality = entry.get("quality")
        city = entry.get("city")
        price = entry.get("sell_price_min", 0)

        if price > 0:
            key = f"{item_id}@{quality}@{city}"
            if key not in best_by_key or price < best_by_key[key]["sell_price_min"]:
                best_by_key[key] = entry

    return list(best_by_key.values())