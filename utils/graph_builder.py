import matplotlib.pyplot as plt
from datetime import datetime
import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

def generate_price_chart(
    data: List[Dict], item_id: str, city: str, output_dir: str = "charts"
) -> Optional[str]:
    """
    Generates and saves a price chart image from timestamped price data.

    Parameters:
        data (List[Dict]): List of dictionaries with 'timestamp' and 'avg_price' keys.
        item_id (str): Unique item identifier.
        city (str): Market city.
        output_dir (str): Directory to save the chart image.

    Returns:
        str or None: Path to saved image, or None if generation fails.
    """
    if not data:
        logger.warning(f"No data to generate chart for {item_id} in {city}.")
        return None

    try:
        # ✅ Filtra entradas válidas com os campos obrigatórios
        filtered_data = [
            entry for entry in data
            if "timestamp" in entry and "avg_price" in entry and isinstance(entry["avg_price"], (int, float))
        ]

        if not filtered_data:
            logger.warning(f"Filtered data is empty or invalid for {item_id} in {city}.")
            return None

        os.makedirs(output_dir, exist_ok=True)

        timestamps = [datetime.fromisoformat(entry["timestamp"]) for entry in filtered_data]
        prices = [entry["avg_price"] for entry in filtered_data]

        plt.figure(figsize=(10, 4))
        plt.plot(timestamps, prices, marker="o", linewidth=1.5)
        plt.title(f"Price Trend — {item_id} in {city}")
        plt.xlabel("Date")
        plt.ylabel("Avg Price (silver)")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.tight_layout()

        filename = f"{item_id}_{city}.png".replace(" ", "_")
        path = os.path.join(output_dir, filename)

        plt.savefig(path)
        plt.close()

        return path

    except Exception as e:
        logger.error(f"Error generating chart for {item_id} in {city}: {e}")
        return None