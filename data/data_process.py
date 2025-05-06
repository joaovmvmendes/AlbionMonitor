from data_fetch.api_history import fetch_item_history
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

def analisar_arbitragem(data, item_variants, min_margin=0.15, max_margin=1.0):
    oportunidades = []
    for item in item_variants:
        item_id = item["item_id"]
        qualidade = item.get("quality", 1)

        ofertas = [
            d for d in data
            if d.get("item_id") == item_id and d.get("sell_price_min", 0) > 0 and d.get("quality") == qualidade
        ]

        print(f"\n📦 {item}: {len(ofertas)} ofertas válidas encontradas.")

        if len(ofertas) < 2:
            print(f"⚠️ Menos de duas ofertas para {item}, ignorando.")
            continue

        ofertas.sort(key=lambda x: x["sell_price_min"])
        origem = ofertas[0]
        destino = ofertas[-1]

        preco_origem = origem["sell_price_min"]
        preco_destino = destino["sell_price_min"]
        lucro = preco_destino - preco_origem
        margem_lucro = lucro / preco_origem

        print(f"💰 {item_id} → Origem: {origem['city']} ({preco_origem}) | Destino: {destino['city']} ({preco_destino}) | Margem: {margem_lucro:.2%}")

        if min_margin <= margem_lucro < max_margin:
            oportunidades.append({
                "item": item_id,
                "origem": origem["city"],
                "destino": destino["city"],
                "preco_origem": preco_origem,
                "preco_destino": preco_destino,
                "lucro": lucro,
                "margem": margem_lucro,
                "quality": qualidade
            })

    print(f"\n✅ Total de oportunidades encontradas: {len(oportunidades)}")
    oportunidades.sort(key=lambda x: x["margem"], reverse=True)

    return oportunidades  # 🔄 Retorna todas as oportunidades

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
        partes = chave.split("@")

        if len(partes) < 2:
            print(f"⚠️ Chave inválida para tendência histórica: {chave}")
            continue

        item = "@".join(partes[:-1])
        cidade = partes[-1]

        if not historico:
            continue

        historico_info = historico[0]["data"]
        if len(historico_info) < 2:
            continue

        preco_inicio = historico_info[-1].get("prices_avg", 0)
        preco_fim = historico_info[0].get("prices_avg", 0)

        if preco_inicio == 0 or preco_fim == 0:
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

        print(f"🔎 Verificando item: {item} em {cidade}")
        for d in historico_info:
            print(f"  📆 {d['timestamp']} | 🛒 {d.get('item_count', 0)} vendidos | 💰 preço médio: {d.get('avg_price', 0)}")

    alertas.sort(key=lambda x: abs(x["variacao"]), reverse=True)
    return alertas

def calcular_media_vendas(item_id, city, quality=1, dias=7):
    historico = fetch_item_history(item_id, city, dias)

    if not historico:
        print(f"[AVISO] Nenhum histórico encontrado para {item_id} em {city} (Qualidade {quality})")
        return None

    contagens = []
    for entrada in historico:
        if entrada.get("quality") != quality:
            continue

        dias_vendas = entrada.get("data", [])[:dias]
        contagens.extend(
            d.get("item_count", 0) for d in dias_vendas if d.get("item_count", 0) > 0
        )

    if not contagens:
        print(f"[AVISO] Sem contagens válidas para {item_id} em {city} (Qualidade {quality})")
        return None

    return sum(contagens) // len(contagens)