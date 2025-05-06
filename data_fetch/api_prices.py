import time
import requests
from config.constants import API_BASE_URL, CITIES

API_BASE = API_BASE_URL
price_cache = {}

def get_item_prices_from_api(item_id, quality=None):
    cache_key = f"{item_id}|{quality or 'any'}"
    if cache_key in price_cache:
        return price_cache[cache_key]

    print(f"🔍 Buscando preços para: {item_id}" + (f" (Qualidade {quality})" if quality else ""))
    params = {"locations": ",".join(CITIES)}
    if quality:
        params["qualities"] = quality

    try:
        response = requests.get(f"{API_BASE}/{item_id}.json", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        price_cache[cache_key] = data
        time.sleep(0.35)
        return data
    except Exception as e:
        print(f"⚠️ Erro ao buscar preço para {item_id}: {e}")
        return []