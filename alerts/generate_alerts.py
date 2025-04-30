from collections import defaultdict

def gerar_alertas(data, item_names, agrupamento="city"):
    print("Iniciando a geração de alertas com agrupamento por", agrupamento)

    if agrupamento != "city":
        print(f"Aviso: agrupamento '{agrupamento}' não implementado ainda.")
        return []

    agrupados = defaultdict(list)

    for item in data:
        item_id = item.get("item_id", "N/A")
        city = item.get("city", "Desconhecida")
        sell_price_min = item.get("sell_price_min", 0)

        if item_id in item_names and sell_price_min > 0:
            mensagem = f"O item {item_id} está com preço mínimo: {sell_price_min}"
            agrupados[city.upper()].append(mensagem)

    if not agrupados:
        print("Nenhum alerta gerado.")
        return []

    mensagens = []
    for cidade in sorted(agrupados.keys()):
        mensagens.append(cidade)  # Nome da cidade em maiúsculas
        mensagens.extend(agrupados[cidade])
        mensagens.append("")  # Linha em branco entre blocos

    return mensagens
