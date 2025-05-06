# utils/item_expander.py

def expand_item_variants(config_items):
    """
    Expands each base item into enchanted and quality variants.
    """
    expanded_items = []
    for item in config_items:
        base_name = item["base_name"]
        quality = item["quality"]

        for enchantment in item["enchantments"]:
            item_id = f"{base_name}@{enchantment}" if enchantment > 0 else base_name
            expanded_items.append({
                "item_id": item_id,
                "base_name": base_name,
                "enchantment": enchantment,
                "quality": quality
            })

    return expanded_items