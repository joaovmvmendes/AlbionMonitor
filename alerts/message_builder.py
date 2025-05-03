def format_arbitragem_alert(oportunidades: list[dict]) -> list[str]:
    mensagens = []
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
        mensagens.append("Nenhuma oportunidade de arbitragem encontrada hoje.")
    return mensagens

def format_price_range_alerts(data, item_names, agrupamento, agrupar_por_func) -> list[str]:
    mensagens = []
    agrupados = agrupar_por_func(data, item_names, agrupamento)
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

def format_trend_alerts(historico, analisar_func, variacao_min) -> list[str]:
    mensagens = []
    tendencias = analisar_func(historico, variacao_min=variacao_min)
    if tendencias:
        mensagens.append("📈 *Tendências de preço nos últimos dias:*")
        for t in tendencias[:10]:
            direcao = "aumento" if t["variacao"] > 0 else "queda"
            mensagens.append(
                f"{t['item']} em {t['cidade']}: {direcao} de "
                f"{t['inicio']:.0f} → {t['fim']:.0f} ({t['variacao']:.1%})"
            )
    return mensagens
