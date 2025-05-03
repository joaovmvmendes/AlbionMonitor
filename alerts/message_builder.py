from data.data_process import calcular_media_vendas

def format_arbitragem_alert(oportunidades):
    if not oportunidades:
        return ["Nenhuma oportunidade de arbitragem encontrada hoje."]

    mensagens = ["🔥 *Top oportunidades de compra e venda do dia:*"]
    
    for idx, o in enumerate(oportunidades, 1):
        media = calcular_media_vendas(o["item"], o["origem"])
        
        if media is None:
            linha_vendas = "Média diária de vendas: dados indisponíveis"
        else:
            linha_vendas = f"Média diária de vendas: {media} un."

        mensagens.append(
            f"{idx}. *{o['item']}*\n"
            f"Comprar em {o['origem']} por `{o['preco_origem']}`\n"
            f"Vender em {o['destino']} por `{o['preco_destino']}`\n"
            f"Lucro: `{o['lucro']}` silver ({o['margem']:.1%})\n"
            f"{linha_vendas}\n"
        )
    
    return ["\n".join(mensagens)]

def format_trend_alerts(historico, analisar_func, variacao_min=0.10):
    tendencias = analisar_func(historico, variacao_min)
    if not tendencias:
        return []

    mensagens = ["📈 *Tendências de preço nos últimos dias:*"]
    for t in tendencias[:10]:
        direcao = "aumento" if t["variacao"] > 0 else "queda"
        mensagens.append(
            f"{t['item']} em {t['cidade']}: {direcao} de "
            f"{t['inicio']:.0f} → {t['fim']:.0f} ({t['variacao']:.1%})"
        )

    return ["\n".join(mensagens)]