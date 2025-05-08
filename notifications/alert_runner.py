import logging
from typing import List, Dict

from config.constants import QUALITY_LABELS
from notifications.telegram import send_telegram_message, send_telegram_photo
from data.data_process import calculate_sales_average
from utils.graph_builder import generate_price_chart
from utils.text_format import build_arbitrage_text

logger = logging.getLogger(__name__)


def run_alerts(
    filtered_market_data: List[Dict],
    item_variants: List[Dict],
    history: Dict[str, Dict]
) -> None:
    """
    For each monitored item, generate and send:
    - A formatted arbitrage message with quality, enchantment, cities, profit and average sales
    - (Temporarily disabled) A chart showing historical price variation in the selling city

    Args:
        filtered_market_data (List[Dict]): List of filtered market offers.
        item_variants (List[Dict]): List of item definitions with quality and IDs.
        history (Dict[str, Dict]): Pre-fetched price history data (grouped by item@city).
    """
    logger.info("📦 Starting alert generation per item...")

    for idx, item in enumerate(item_variants, start=1):
        item_id = item["item_id"]
        quality = item.get("quality", 1)

        # Extract enchantment from item_id (e.g., T4_BAG@3 → enchantment 3)
        if "@" in item_id:
            base_name, enchantment = item_id.split("@")
            enchantment = int(enchantment)
        else:
            base_name = item_id
            enchantment = None

        # Filter offers for this item and quality
        offers = [
            o for o in filtered_market_data
            if o["item_id"] == item_id and o.get("quality") == quality
        ]

        if not offers:
            logger.warning(f"No market data for item {item_id} (Q{quality})")
            lowest_offer = highest_offer = {"city": None, "sell_price_min": None}
        else:
            lowest_offer = min(offers, key=lambda x: x.get("sell_price_min", float("inf")))
            highest_offer = max(offers, key=lambda x: x.get("sell_price_min", 0))

        origin_price = lowest_offer.get("sell_price_min")
        destination_price = highest_offer.get("sell_price_min")

        origin_city = lowest_offer.get("city")
        destination_city = highest_offer.get("city")

        profit = None
        margin = 0.0
        if origin_price and destination_price and destination_price > origin_price:
            profit = destination_price - origin_price
            margin = profit / origin_price
            if margin > 10.0:
                margin = 10.0  # Cap margin at 1000%

        # Get average daily sales using cached history
        history_key = f"{item_id}@{destination_city}"
        history_cache = history.get(history_key, {}).get("data", [])
        avg_sales = calculate_sales_average(
            item_id,
            destination_city,
            quality,
            history_cache=history_cache
        )
        sales_line = (
            f"Average daily sales: {avg_sales} units"
            if avg_sales is not None else
            "Average daily sales: data unavailable"
        )

        quality_label = QUALITY_LABELS.get(quality, "Normal")

        opportunity_data = {
            "item": item_id,
            "origin": origin_city,
            "destination": destination_city,
            "origin_price": origin_price,
            "destination_price": destination_price,
            "profit": profit,
            "margin": margin,
            "quality": quality,
        }

        message = build_arbitrage_text(
            index=idx,
            base_name=base_name,
            enchantment=enchantment,
            quality_str=quality_label,
            opportunity=opportunity_data,
            sales_line=sales_line,
        )

        send_telegram_message(message)

        # Chart generation is temporarily disabled
        # chart_data = history_cache
        # logger.debug(f"📊 Raw chart data for {item_id}@{destination_city}: {chart_data}")
        # image_path = generate_price_chart(chart_data, item_id, destination_city)
        # if image_path:
        #     send_telegram_photo(image_path)

    logger.info("✅ Alert flow finished.")