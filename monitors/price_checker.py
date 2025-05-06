from data_fetch.api_prices import get_item_prices_from_api
from data_fetch.api_history import fetch_item_history
from alerts.alert_runner import run_alerts
from config.constants import CITIES

def fetch_market_data(item_variants):
    todos_dados = []
    for item in item_variants:
        item_id = item["item_id"]
        qualidade = item.get("quality")
        print(f"🔍 Buscando preços para: {item_id} (Qualidade {qualidade})")
        dados = get_item_prices_from_api(item_id, qualidade)
        todos_dados.extend(dados)
    return todos_dados

def fetch_all_history(item_variants, dias=7):
    historico = {}

    for item in item_variants:
        item_id = item["item_id"]
        qualidade = item.get("quality", 1)

        for cidade in CITIES:
            chave = f"{item_id}@{cidade}"
            print(f"📈 Buscando histórico: {chave} (Qualidade {qualidade})")
            dados = fetch_item_history(item_id, cidade, dias)
            historico[chave] = [{
                "item_id": item_id,
                "city": cidade,
                "quality": qualidade,
                "data": dados
            }]

    return historico

def filtrar_melhores_ofertas(data):
    """
    Mantém apenas a melhor (menor) oferta por cidade.
    """
    por_chave = {}

    for d in data:
        item_id = d.get("item_id")
        qualidade = d.get("quality")
        cidade = d.get("city")
        preco = d.get("sell_price_min", 0)

        if preco > 0:
            chave = f"{item_id}@{qualidade}@{cidade}"
            if chave not in por_chave or preco < por_chave[chave]["sell_price_min"]:
                por_chave[chave] = d

    return list(por_chave.values())

def run_price_monitor(item_variants):
    print("🔄 Coletando dados de mercado...")
    market_data = fetch_market_data(item_variants)

    # ✅ Mantém apenas as melhores ofertas por item/qualidade/cidade
    dados_filtrados = filtrar_melhores_ofertas(market_data)

    print("📈 Coletando históricos de venda...")
    historico = fetch_all_history(item_variants)

    # ✅ Gera e envia alertas com os dados processados
    run_alerts(dados_filtrados, item_variants, historico=historico)