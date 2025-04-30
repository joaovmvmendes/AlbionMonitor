def gerar_alertas(data, item_names):
    alertas = []
    print("Iniciando a geração de alertas...")

    for item in data:
        item_id = item.get("item_id", "N/A")
        city = item.get("city", "Desconhecida")
        sell_price_min = item.get("sell_price_min", 0)

        print(f"Item: {item_id}, Cidade: {city}, Preço Mínimo: {sell_price_min}")

        if item_id in item_names and sell_price_min > 0:
            alerta = f"⚠️ O item {item_id} em {city} está com preço mínimo: {sell_price_min}"
            alertas.append(alerta)
            print("Alerta gerado:", alerta)

    if not alertas:
        print("Nenhum alerta gerado.")
    return alertas
