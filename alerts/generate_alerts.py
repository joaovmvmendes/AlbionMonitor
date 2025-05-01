from collections import defaultdict
import os

# Define o lucro percentual mínimo, exemplo: 0.15 = 15%
MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.15))
MAX_PROFIT_MARGIN = float(os.getenv("MAX_PROFIT_MARGIN", 10))

def gerar_alertas(data, item_names, agrupamento=None):
    def _gerar_alerta_compra_e_venda(mensagens, data, item_names):
        print("Iniciando a geração de alertas de compra e venda")

        oportunidades = []
        for item_name in item_names:
            # Filtrar os dados relevantes para o item
            ofertas = [
                d for d in data
                if d.get("item_id") == item_name and d.get("sell_price_min", 0) > 0
            ]

            if len(ofertas) < 2:
                continue

            # Ordenar por menor preço de venda
            ofertas.sort(key=lambda x: x["sell_price_min"])
            origem = ofertas[0]
            destino = ofertas[-1]

            preco_origem = origem["sell_price_min"]
            preco_destino = destino["sell_price_min"]
            lucro = preco_destino - preco_origem
            margem_lucro = lucro / preco_origem
            
            if (margem_lucro >= MIN_PROFIT_MARGIN) and (margem_lucro < MAX_PROFIT_MARGIN):
                oportunidades.append(
                    {
                        "item": item_name,
                        "origem": origem["city"],
                        "destino": destino["city"],
                        "preco_origem": preco_origem,
                        "preco_destino": preco_destino,
                        "lucro": lucro,
                        "margem": margem_lucro
                    }
                )

        # Ordenar por maior margem de lucro percentual
        oportunidades.sort(key=lambda x: x["margem"], reverse=True)

        # Selecionar top 3
        top_oportunidades = oportunidades[:3]

        if not top_oportunidades:
            mensagens.append("Nenhuma oportunidade de compra e venda com margem suficiente encontrada.")
        else:
            mensagens.append(f"🔥 *Top {len(top_oportunidades)} oportunidades de compra e venda do dia:*")
            for i, op in enumerate(top_oportunidades, start=1):
                mensagens.append(
                    f"{i}. *{op['item']}*\n"
                    f"Comprar em {op['origem']} por `{op['preco_origem']}`\n"
                    f"Vender em {op['destino']} por `{op['preco_destino']}`\n"
                    f"Lucro: `{op['lucro']}` silver ({op['margem']:.1%})\n"
                )

        return mensagens
    
    def _gerar_alerta_preços_itens(mensagens, data, item_names, agrupamento):
    
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

        for chave in sorted(agrupados.keys()):
            mensagens.append(chave)  # título do grupo
            mensagens.extend(agrupados[chave])
            mensagens.append("")  # linha em branco entre grupos

        return mensagens
    
    mensagens = []
    _gerar_alerta_compra_e_venda(mensagens=mensagens, data=data, item_names=item_names)
    _gerar_alerta_preços_itens(mensagens=mensagens, data=data, item_names=item_names, agrupamento=agrupamento)

    return mensagens
