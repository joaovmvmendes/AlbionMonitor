from data.data_process import calculate_sales_average
from data_fetch.api_charts import fetch_item_chart_data
from utils.graph_builder import generate_price_chart
from config.constants import QUALITY_LABELS

def format_arbitrage_alerts(opportunities):
    if not opportunities:
        return [("Nenhuma oportunidade de arbitragem encontrada hoje.", None)]

    results = []

    for idx, opportunity in enumerate(opportunities, 1):
        # Calculate average daily sales at the destination city
        avg_sales = calculate_sales_average(opportunity["item"], opportunity["destino"], opportunity["quality"])
        sales_line = (
            f"Média diária de vendas: {avg_sales} un." if avg_sales is not None
            else "Média diária de vendas: dados indisponíveis"
        )

        # Split item and enchantment if present
        if "@" in opportunity["item"]:
            base_name, enchantment = opportunity["item"].split("@")
            enchantment_str = f" (Encantado +{enchantment})"
        else:
            base_name = opportunity["item"]
            enchantment_str = ""

        quality = opportunity.get("quality", 1)
        quality_str = QUALITY_LABELS.get(quality, "Normal")

        # Use only base item name for chart (API does not accept @n)
        item_base = base_name
        chart_data = fetch_item_chart_data(item_base, opportunity["destino"], opportunity["quality"])
        image_path = generate_price_chart(chart_data, item_base, opportunity["destino"])

        text = (
            f"{idx}. *{base_name}{enchantment_str}* — Qualidade: {quality_str}\n"
            f"Comprar em {opportunity['origem']} por `{opportunity['preco_origem']}`\n"
            f"Vender em {opportunity['destino']} por `{opportunity['preco_destino']}`\n"
            f"Lucro: `{opportunity['lucro']}` silver ({opportunity['margem']:.1%})\n"
            f"{sales_line}\n"
        )

        results.append((text, image_path))

    return results

def format_trend_alerts(history, analyze_function, min_variation=0.10):
    trends = analyze_function(history, min_variation)
    if not trends:
        return []

    messages = ["📈 *Tendências de preço nos últimos dias:*"]
    for trend in trends[:10]:
        direction = "aumento" if trend["variacao"] > 0 else "queda"
        messages.append(
            f"{trend['item']} em {trend['cidade']}: {direction} de "
            f"{trend['inicio']:.0f} → {trend['fim']:.0f} ({trend['variacao']:.1%})"
        )

    return ["\n".join(messages)]