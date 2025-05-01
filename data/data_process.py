import json
import os
from collections import defaultdict

STATE_FILE = "last_state.json"

def load_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_current_state(data):
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f)

def analisar_arbitragem(data, item_names, min_margin=0.15, max_margin=10):
    oportunidades = []
    for item_name in item_names:
        ofertas = [
            d for d in data
            if d.get("item_id") == item_name and d.get("sell_price_min", 0) > 0
        ]

        if len(ofertas) < 2:
            continue

        ofertas.sort(key=lambda x: x["sell_price_min"])
        origem = ofertas[0]
        destino = ofertas[-1]

        preco_origem = origem["sell_price_min"]
        preco_destino = destino["sell_price_min"]
        lucro = preco_destino - preco_origem
        margem_lucro = lucro / preco_origem

        if min_margin <= margem_lucro < max_margin:
            oportunidades.append({
                "item": item_name,
                "origem": origem["city"],
                "destino": destino["city"],
                "preco_origem": preco_origem,
                "preco_destino": preco_destino,
                "lucro": lucro,
                "margem": margem_lucro
            })

    oportunidades.sort(key=lambda x: x["margem"], reverse=True)
    return oportunidades[:3]

def agrupar_por(data, item_names, agrupamento):
    agrupados = defaultdict(list)

    if agrupamento not in ("city", "item"):
        return agrupados

    for item in data:
        item_id = item.get("item_id")
        city = item.get("city", "Desconhecida")
        sell_price_min = item.get("sell_price_min", 0)
        sell_price_max = item.get("sell_price_max", 0)

        if item_id in item_names and sell_price_min >= 0:
            chave = city.upper() if agrupamento == "city" else item_id.upper()
            agrupados[chave].append({
                "min": sell_price_min,
                "max": sell_price_max,
                "item": item_id
            })

    return agrupados
