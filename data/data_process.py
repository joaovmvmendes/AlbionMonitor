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

def analisar_tendencia_historica(historicos_por_item, variacao_min=0.10):
    alertas = []
    for chave, historico in historicos_por_item.items():
        item, cidade = chave.split("@")

        if not historico:
            continue

        historico_info = historico[0]["data"]
        if len(historico_info) < 2:
            continue

        preco_inicio = historico_info[-1]["avg_price"]
        preco_fim = historico_info[0]["avg_price"]

        if preco_inicio == 0:
            continue

        variacao = (preco_fim - preco_inicio) / preco_inicio

        if abs(variacao) >= variacao_min:
            alertas.append({
                "item": item,
                "cidade": cidade,
                "inicio": preco_inicio,
                "fim": preco_fim,
                "variacao": variacao
            })

    alertas.sort(key=lambda x: abs(x["variacao"]), reverse=True)
    return alertas
