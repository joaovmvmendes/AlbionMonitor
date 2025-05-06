def filter_best_offers(data):
    """
    Keeps only the best (lowest) offer per item-quality-city combination.
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