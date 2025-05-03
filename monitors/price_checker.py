from data_fetch.api_prices import get_item_prices_from_api
from data.data_process import analisar_arbitragem
from alerts.message_builder import format_arbitragem_alert
from config.settings import MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN

def filtrar_melhores_ofertas(data):
    por_cidade = {}
    for d in data:
        cidade = d["city"]
        preco = d.get("sell_price_min")
        if preco and preco > 0:
            if cidade not in por_cidade or preco < por_cidade[cidade]["sell_price_min"]:
                por_cidade[cidade] = d
    return list(por_cidade.values())

def run_price_monitor(item_variants):
    todas_oportunidades = []

    for item in item_variants:
        item_id = item["item_id"]
        qualidade = item.get("quality", None)
        
        data = get_item_prices_from_api(item_id, qualidade=None)
        qualidade_desejada = item.get("quality")
        filtrados = [d for d in data if d.get("quality") == qualidade_desejada]
        melhores = filtrar_melhores_ofertas(filtrados)

        
        oportunidades = analisar_arbitragem(melhores, [item_id], MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN)
        todas_oportunidades.extend(oportunidades)

    mensagens = format_arbitragem_alert(todas_oportunidades)
    return mensagens
