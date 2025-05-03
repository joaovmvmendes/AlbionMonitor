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

def run_price_monitor(item_names):
    todas_oportunidades = []

    for item in item_names:
        data = get_item_prices_from_api(item, qualidade=None)
        melhores = filtrar_melhores_ofertas(data)
        oportunidades = analisar_arbitragem(melhores, [item], MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN)
        todas_oportunidades.extend(oportunidades)

    mensagens = format_arbitragem_alert(todas_oportunidades)
    return mensagens
