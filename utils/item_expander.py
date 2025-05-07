import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def expand_item_variants(config_items: List[Dict]) -> List[Dict]:
    """
    Expands a list of base items into all combinations of enchantments and quality levels.

    Parameters:
        config_items (List[Dict]): Each dictionary must contain 'base_name', 'enchantments', and 'quality'.

    Returns:
        List[Dict]: Expanded item variants with keys: item_id, base_name, enchantment, quality.
    """
    expanded = []

    for item in config_items:
        base_name = item.get("base_name")
        enchantments = item.get("enchantments", [])
        quality = item.get("quality")

        if not base_name or quality is None:
            logger.warning(f"Invalid item configuration found: {item}")
            continue

        for enchant in enchantments:
            item_id = f"{base_name}@{enchant}" if enchant > 0 else base_name
            expanded.append({
                "item_id": item_id,
                "base_name": base_name,
                "enchantment": enchant,
                "quality": quality
            })

    return expanded