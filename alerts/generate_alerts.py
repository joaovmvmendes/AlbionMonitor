import os
from data.data_process import analisar_arbitragem, agrupar_por

MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.15))
MAX_PROFIT_MARGIN = float(os.getenv("MAX_PROFIT_MARGIN", 10))

def gerar_alertas(data, item_names, agrupamento=None):
    mensagens = []

    oportunidades = analisar_arbitragem(data, item_names, MIN_PROFIT_MARGIN, MAX_PROFIT_MARGIN)
    if oportunidades:
        mensagens.append(f"🔥 *Top {len(oportunidades)} oportunidades de compra e venda do dia:*")
        for i, op in enumerate(oportunidades, start=1):
            mensagens.append(
                f"{i}. *{op['item']}*\n"
                f"Comprar em {op['origem']} por `{op['preco_origem']}`\n"
                f"Vender em {op['destino']} por `{op['preco_destino']}`\n"
                f"Lucro: `{op['lucro']}` silver ({op['margem']:.1%})\n"
            )
    else:
        mensagens.append("Nenhuma oportunidade de compra e venda com margem suficiente encontrada.")

    agrupados = agrupar_por(data, item_names, agrupamento)
    if agrupados:
        for chave, itens in sorted(agrupados.items()):
            mensagens.append(f"{chave}")
            for item in itens:
                mensagens.append(
                    f"Você pode vender o item {item['item']} pelo valor mínimo de: {item['min']} via SellOrder"
                )
                mensagens.append(
                    f"Você pode vender o item {item['item']} pelo valor máximo de: {item['max']} via SellOrder"
                )
            mensagens.append("")

    return mensagens
