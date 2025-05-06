from data.data_process import calculate_sales_average
from services.albion_api import get_item_chart
from utils.graph_builder import generate_price_chart
from config.constants import QUALITY_LABELS
from utils.text_format import build_arbitrage_text

def format_arbitrage_alerts(opportunities):
    if not opportunities:
        return [("Nenhuma oportunidade de arbitragem encontrada hoje.", None)]

    results = []

    for idx, opportunity in enumerate(opportunities, 1):
        avg_sales = calculate_sales_average(opportunity["item"], opportunity["destino"], opportunity["quality"])
        sales_line = (
            f"Média diária de vendas: {avg_sales} un." if avg_sales is not None
            else "Média diária de vendas: dados indisponíveis"
        )

        # Parse base name and enchantment
        if "@" in opportunity["item"]:
            base_name, enchantment = opportunity["item"].split("@")
        else:
            base_name = opportunity["item"]
            enchantment = None

        quality = opportunity.get("quality", 1)
        quality_str = QUALITY_LABELS.get(quality, "Normal")

        chart_data = get_item_chart(base_name, opportunity["destino"], quality)
        image_path = generate_price_chart(chart_data, base_name, opportunity["destino"])

        text = build_arbitrage_text(idx, base_name, enchantment, quality_str, opportunity, sales_line)

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