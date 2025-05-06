from services.albion_api import get_item_prices, get_item_history
from notifications.alert_runner import run_alerts
from config.constants import CITIES
from utils.filters import filter_best_offers

def fetch_market_data(item_variants):
    all_data = []
    for item in item_variants:
        item_id = item["item_id"]
        quality = item.get("quality")
        print(f"🔍 Buscando preços para: {item_id}" + (f" (Qualidade {quality})" if quality else ""))
        data = get_item_prices(item_id, quality)
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
            data = get_item_history(item_id, city, days)
            history[key] = [{
                "item_id": item_id,
                "city": city,
                "quality": quality,
                "data": data
            }]

    return history

def run_price_monitor(item_variants):
    print("🔄 Coletando dados de mercado...")
    market_data = fetch_market_data(item_variants)

    # ✅ Filtra melhores ofertas
    filtered_data = filter_best_offers(market_data)

    print("📈 Coletando históricos de venda...")
    history = fetch_all_history(item_variants)

    # ✅ Executa alertas com os dados processados
    run_alerts(filtered_data, item_variants, history=history)