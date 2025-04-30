from collections import defaultdict

def gerar_alertas(data, item_names, agrupamento="city"):
    print("Iniciando a geração de alertas com agrupamento por", agrupamento)

    if agrupamento not in ("city", "item"):
        print(f"Aviso: agrupamento '{agrupamento}' não é suportado.")
        return []

    agrupados = defaultdict(list)

    for item in data:
        item_id = item.get("item_id", "N/A")
        city = item.get("city", "Desconhecida")
        sell_price_min = item.get("sell_price_min", 0)

        if item_id in item_names and sell_price_min > 0:
            mensagem = f"O item {item_id} está com preço mínimo: {sell_price_min}"

            if agrupamento == "city":
                chave = city.upper()
            else:  # agrupamento == "item"
                chave = item_id.upper()

            agrupados[chefe := chave].append(mensagem)

    if not agrupados:
        print("Nenhum alerta gerado.")
        return []

    mensagens = []
    for chave in sorted(agrupados.keys()):
        mensagens.append(chave)  # título do grupo
        mensagens.extend(agrupados[chave])
        mensagens.append("")  # linha em branco entre grupos

    return mensagens
