from collections import defaultdict

def gerar_alertas(data, item_names, agrupamento):
    print("Iniciando a geração de alertas com agrupamento por", agrupamento)

    if agrupamento not in ("city", "item"):
        print(f"Aviso: agrupamento '{agrupamento}' não é suportado.")
        return []

    agrupados = defaultdict(list)

    for item in data:
        item_id = item.get("item_id", "N/A")
        city = item.get("city", "Desconhecida")
        sell_price_min = item.get("sell_price_min", 0)
        sell_price_max = item.get("sell_price_max", 0)
        #buy_price_min = item.get("buy_price_min", 0)
        #buy_price_max = item.get("buy_price_max", 0)

        if item_id in item_names and sell_price_min >= 0:
            mensagens_item = [
                f"Você pode vender o item {item_id} pelo valor mínimo de: {sell_price_min} via SellOrder",
                f"Você pode vender o item {item_id} pelo valor máximo de: {sell_price_max} via SellOrder"
            ]

            chave = city.upper() if agrupamento == "city" else item_id.upper()
            agrupados[chave].extend(mensagens_item)

    if not agrupados:
        print("Nenhum alerta gerado.")
        return []

    mensagens = []
    for chave in sorted(agrupados.keys()):
        mensagens.append(chave)  # título do grupo
        mensagens.extend(agrupados[chave])
        mensagens.append("")  # linha em branco entre grupos

    return mensagens
