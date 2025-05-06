from services.albion_api import get_item_history
from collections import defaultdict

def analyze_arbitrage(data, item_variants, min_margin=0.15, max_margin=1.0):
    opportunities = []
    for variant in item_variants:
        item_id = variant["item_id"]
        quality = variant.get("quality", 1)

        offers = [
            entry for entry in data
            if entry.get("item_id") == item_id and entry.get("sell_price_min", 0) > 0 and entry.get("quality") == quality
        ]

        print(f"\n📦 {variant}: {len(offers)} ofertas válidas encontradas.")

        if len(offers) < 2:
            print(f"⚠️ Menos de duas ofertas para {variant}, ignorando.")
            continue

        offers.sort(key=lambda x: x["sell_price_min"])
        origin = offers[0]
        destination = offers[-1]

        origin_price = origin["sell_price_min"]
        destination_price = destination["sell_price_min"]
        profit = destination_price - origin_price
        profit_margin = profit / origin_price

        print(f"💰 {item_id} → Origem: {origin['city']} ({origin_price}) | Destino: {destination['city']} ({destination_price}) | Margem: {profit_margin:.2%}")

        if min_margin <= profit_margin < max_margin:
            opportunities.append({
                "item": item_id,
                "origem": origin["city"],
                "destino": destination["city"],
                "preco_origem": origin_price,
                "preco_destino": destination_price,
                "lucro": profit,
                "margem": profit_margin,
                "quality": quality
            })

    print(f"\n✅ Total de oportunidades encontradas: {len(opportunities)}")
    opportunities.sort(key=lambda x: x["margem"], reverse=True)

    return opportunities

def group_by(data, item_names, group_key):
    grouped = defaultdict(list)

    if group_key not in ("city", "item"):
        return grouped

    for item in data:
        item_id = item.get("item_id")
        city = item.get("city", "Desconhecida")
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

def analyze_historical_trend(item_histories, min_variation=0.10):
    alerts = []
    for key, history in item_histories.items():
        parts = key.split("@")

        if len(parts) < 2:
            print(f"⚠️ Chave inválida para tendência histórica: {key}")
            continue

        item = "@".join(parts[:-1])
        city = parts[-1]

        if not history:
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
                "cidade": city,
                "inicio": start_price,
                "fim": end_price,
                "variacao": variation
            })

        print(f"🔎 Verificando item: {item} em {city}")
        for d in history_info:
            print(f"  📆 {d['timestamp']} | 🛒 {d.get('item_count', 0)} vendidos | 💰 preço médio: {d.get('avg_price', 0)}")

    alerts.sort(key=lambda x: abs(x["variacao"]), reverse=True)
    return alerts

def calculate_sales_average(item_id, city, quality=1, days=7):
    history = get_item_history(item_id, city, days)

    if not history:
        print(f"[AVISO] Nenhum histórico encontrado para {item_id} em {city} (Qualidade {quality})")
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
        print(f"[AVISO] Sem contagens válidas para {item_id} em {city} (Qualidade {quality})")
        return None

    return sum(counts) // len(counts)