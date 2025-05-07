from typing import List, Tuple, Optional, Dict, Callable

from data.data_process import calculate_sales_average
from services.albion_api import get_item_chart
from utils.graph_builder import generate_price_chart
from config.constants import QUALITY_LABELS
from utils.text_format import build_arbitrage_text

def format_arbitrage_alerts(opportunities: List[Dict]) -> List[Tuple[str, Optional[str]]]:
    """
    Formats arbitrage alerts for each opportunity, with optional chart image.

    Returns:
        List of (message, image_path) tuples.
    """
    if not opportunities:
        return [("No arbitrage opportunities found today.", None)]

    results = []

    for idx, opportunity in enumerate(opportunities, 1):
        avg_sales = calculate_sales_average(opportunity["item"], opportunity["destination"], opportunity["quality"])
        sales_line = (
            f"Average daily sales: {avg_sales} units" if avg_sales is not None
            else "Average daily sales: data unavailable"
        )

        if "@" in opportunity["item"]:
            base_name, enchantment = opportunity["item"].split("@")
        else:
            base_name = opportunity["item"]
            enchantment = None

        quality = opportunity.get("quality", 1)
        quality_str = QUALITY_LABELS.get(quality, "Normal")

        chart_data = get_item_chart(base_name, opportunity["destination"], quality)
        image_path = generate_price_chart(chart_data, base_name, opportunity["destination"])

        text = build_arbitrage_text(idx, base_name, enchantment, quality_str, opportunity, sales_line)
        results.append((text, image_path))

    return results

def format_trend_alerts(
    history: Dict[str, List[Dict]],
    analyze_function: Callable,
    min_variation: float = 0.10
) -> List[str]:
    """
    Formats a list of price trends based on historical data.

    Returns:
        List containing a single Markdown-formatted message string.
    """
    trends = analyze_function(history, min_variation)
    if not trends:
        return []

    messages = ["📈 *Price trends over the last few days:*"]
    for trend in trends[:10]:
        direction = "increase" if trend["variation"] > 0 else "decrease"
        messages.append(
            f"{trend['item']} in {trend['city']}: {direction} from "
            f"{trend['start_price']:.0f} → {trend['end_price']:.0f} ({trend['variation']:.1%})"
        )

    return ["\n".join(messages)]