import os
from data.data_process import analisar_arbitragem, agrupar_por, analisar_tendencia_historica

MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.15))
MAX_PROFIT_MARGIN = float(os.getenv("MAX_PROFIT_MARGIN", 10))

def gerar_alertas(data, item_names, agrupamento=None, historico=None):

    def _gerar_alerta_compra_e_venda(data, item_names, mensagens):
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

    def _gerar_alerta_preços_itens(data, item_names, agrupamento, mensagens):
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
    
    def _gerar_alerta_tendencia_historica(historico, mensagens):
        tendencias = analisar_tendencia_historica(historico, variacao_min=MIN_PROFIT_MARGIN)

        if tendencias:
            mensagens.append("📈 *Tendências de preço nos últimos dias:*")
            for t in tendencias[:3]:
                direcao = "aumento" if t["variacao"] > 0 else "queda"
                mensagens.append(
                    f"{t['item']} em {t['cidade']}: {direcao} de "
                    f"{t['inicio']:.0f} → {t['fim']:.0f} ({t['variacao']:.1%})"
                )

    mensagens = []
    _gerar_alerta_compra_e_venda(data=data, item_names=item_names, mensagens=mensagens)
    _gerar_alerta_preços_itens(data=data, item_names=item_names, agrupamento=agrupamento, mensagens=mensagens)
    _gerar_alerta_tendencia_historica(historico=historico, mensagens=mensagens)

    return mensagens
