import requests

def fetch_item_chart_data(item_id, city, quality=1, days=3):
    """
    Fetches average hourly price history (last N days) for an item in a given city.
    The API does not accept enchantment suffix (@X), so it is removed if present.
    """
    base_item = item_id.split("@")[0]  # Remove enchantment if present

    url = f"https://west.albion-online-data.com/api/v2/stats/charts/{base_item}"
    params = {
        "locations": city,
        "qualities": quality,
        "time-scale": 1  # 1 = hourly
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
                    print(f"[AVISO] Dados inconsistentes para {base_item}@{city}")
                    return []

                return [
                    {"timestamp": ts, "avg_price": price}
                    for ts, price in zip(timestamps[-24 * days:], prices[-24 * days:])
                ]

    except Exception as e:
        print(f"[ERRO] charts API: {base_item}@{city}: {e}")

    return []