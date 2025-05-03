from data_fetch.api_prices import get_item_prices_from_api
from data.data_process import analisar_arbitragem
from alerts.message_builder import format_arbitragem_alert
from alerts.telegram import send_telegram_message
from config.settings import MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN
import os

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
    todas_mensagens = []

    for item in item_names:
        data = get_item_prices_from_api(item, qualidade=None)

        print(f"[DEBUG] {item} retornou {len(data)} entradas da API")
        if data:
            print("[DEBUG] Exemplo:", data[0])
            cidades = {d["city"] for d in data}
            print(f"[DEBUG] {item} encontrado em cidades: {sorted(cidades)}")

        melhores = filtrar_melhores_ofertas(data)

        oportunidades = analisar_arbitragem(melhores, [item], MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN)
        print(f"[DEBUG] {item} → {len(oportunidades)} oportunidades encontradas")

        mensagens = format_arbitragem_alert(oportunidades)
        todas_mensagens.extend(mensagens)

    if todas_mensagens:
        texto_final = "\n\n".join(todas_mensagens)
        send_telegram_message(texto_final)
