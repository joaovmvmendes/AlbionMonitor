def gerar_alertas(data):
    alertas = []

    for item in data:
        item_id = item.get("item_id", "N/A")
        city = item.get("city", "Desconhecida")
        sell_price_min = item.get("sell_price_min", 0)

        print(f"Item: {item_id}, Cidade: {city}, Preço Mínimo: {sell_price_min}")

        if item_id == ITEM_NAME:
            alerta = f"⚠️ O item {item_id} em {city} está com preço mínimo: {sell_price_min}"
            alertas.append(alerta)
            print("Alerta gerado:", alerta)

    return alertas