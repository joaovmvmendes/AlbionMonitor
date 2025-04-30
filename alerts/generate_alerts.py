def gerar_alertas(data, item_name):
    alertas = []
    print("Iniciando a geração de alertas...")  # Log para garantir que entrou na função

    for item in data:
        item_id = item.get("item_id", "N/A")
        city = item.get("city", "Desconhecida")
        sell_price_min = item.get("sell_price_min", 0)

        print(f"Item: {item_id}, Cidade: {city}, Preço Mínimo: {sell_price_min}")

        if item_id == item_name:
            alerta = f"⚠️ O item {item_id} em {city} está com preço mínimo: {sell_price_min}"
            alertas.append(alerta)
            print("Alerta gerado:", alerta)  # Confirme que está gerando alertas

    if not alertas:
        print("Nenhum alerta gerado.")  # Verifique se nenhum alerta está sendo gerado
    return alertas

