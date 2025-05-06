from data.data_process import calcular_media_vendas
from data_fetch.api_charts import fetch_item_chart_data
from utils.graph_builder import gerar_grafico_precos
from config.constants import QUALITY_LABELS

def format_arbitragem_alert(oportunidades):
    if not oportunidades:
        return [("Nenhuma oportunidade de arbitragem encontrada hoje.", None)]

    resultados = []

    for idx, o in enumerate(oportunidades, 1):
        # Calcula média diária de vendas na CIDADE DE VENDA
        media = calcular_media_vendas(o["item"], o["destino"], o["quality"])
        linha_vendas = (
            f"Média diária de vendas: {media} un." if media is not None
            else "Média diária de vendas: dados indisponíveis"
        )

        # Divide item e encantamento, se existir
        if "@" in o["item"]:
            base, enc = o["item"].split("@")
            enc_str = f" (Encantado +{enc})"
        else:
            base = o["item"]
            enc_str = ""

        qualidade = o.get("quality", 1)
        qualidade_str = QUALITY_LABELS.get(qualidade, "Normal")

        # Usa somente o base name para o gráfico (API não aceita @n)
        item_base = base
        chart_data = fetch_item_chart_data(item_base, o["destino"], o["quality"])
        img_path = gerar_grafico_precos(chart_data, item_base, o["destino"])

        texto = (
            f"{idx}. *{base}{enc_str}* — Qualidade: {qualidade_str}\n"
            f"Comprar em {o['origem']} por `{o['preco_origem']}`\n"
            f"Vender em {o['destino']} por `{o['preco_destino']}`\n"
            f"Lucro: `{o['lucro']}` silver ({o['margem']:.1%})\n"
            f"{linha_vendas}\n"
        )

        resultados.append((texto, img_path))

    return resultados

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