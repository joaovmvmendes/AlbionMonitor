from data_fetch.api_prices import get_item_prices_from_api
from data_fetch.api_history import fetch_item_history
from notifications.alert_runner import run_alerts
from config.constants import CITIES

def fetch_market_data(item_variants):
    all_data = []
    for item in item_variants:
        item_id = item["item_id"]
        quality = item.get("quality")
        print(f"🔍 Buscando preços para: {item_id} (Qualidade {quality})")
        data = get_item_prices_from_api(item_id, quality)
        all_data.extend(data)
    return all_data

def fetch_all_history(item_variants, days=7):
    history = {}

    for item in item_variants:
        item_id = item["item_id"]
        quality = item.get("quality", 1)

        for city in CITIES:
            key = f"{item_id}@{city}"
            print(f"📈 Buscando histórico: {key} (Qualidade {quality})")
            data = fetch_item_history(item_id, city, days)
            history[key] = [{
                "item_id": item_id,
                "city": city,
                "quality": quality,
                "data": data
            }]

    return history

def filter_best_offers(data):
    """
    Keeps only the best (lowest) offer per city.
    """
    by_key = {}

    for entry in data:
        item_id = entry.get("item_id")
        quality = entry.get("quality")
        city = entry.get("city")
        price = entry.get("sell_price_min", 0)

        if price > 0:
            key = f"{item_id}@{quality}@{city}"
            if key not in by_key or price < by_key[key]["sell_price_min"]:
                by_key[key] = entry

    return list(by_key.values())

def run_price_monitor(item_variants):
    print("🔄 Coletando dados de mercado...")
    market_data = fetch_market_data(item_variants)

    # ✅ Keeps only the best offers per item/quality/city
    filtered_data = filter_best_offers(market_data)

    print("📈 Coletando históricos de venda...")
    history = fetch_all_history(item_variants)

    # ✅ Generates and sends notifications with processed data
    run_alerts(filtered_data, item_variants, history=history)