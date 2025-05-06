import requests
import time
from config.constants import CITIES

API_BASE_PRICE = "https://west.albion-online-data.com/api/v2/stats/prices"
API_BASE_HISTORY = "https://west.albion-online-data.com/api/v2/stats/history"
API_BASE_CHARTS = "https://west.albion-online-data.com/api/v2/stats/charts"

_price_cache = {}

def get_item_prices(item_id, quality=None):
    key = f"{item_id}|{quality or 'any'}"
    if key in _price_cache:
        return _price_cache[key]

    print(f"🔍 Buscando preços para: {item_id}" + (f" (Qualidade {quality})" if quality else ""))
    params = {"locations": ",".join(CITIES)}
    if quality:
        params["qualities"] = quality

    try:
        response = requests.get(f"{API_BASE_PRICE}/{item_id}.json", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        _price_cache[key] = data
        time.sleep(0.35)
        return data
    except Exception as e:
        print(f"⚠️ Erro ao buscar preço para {item_id}: {e}")
        return []

def get_item_history(item_id, city, days=7):
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
    except Exception as e:
        print(f"[ERRO] API histórico {item_id}@{city}: {e}")
        return []

def get_item_chart(item_id, city, quality=1, days=3):
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
                    print(f"[AVISO] Dados inconsistentes para {base_name}@{city}")
                    return []

                return [
                    {"timestamp": ts, "avg_price": price}
                    for ts, price in zip(timestamps[-24 * days:], prices[-24 * days:])
                ]
    except Exception as e:
        print(f"[ERRO] charts API: {base_name}@{city}: {e}")

    return []