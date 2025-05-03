# utils/item_expander.py

def expand_item_variants(config_items):
    """
    Expande cada item base em variantes com encantamento e qualidade
    """
    expanded = []
    for item in config_items:
        for enchant in item["enchantments"]:
            name = item["base_name"]
            item_id = f"{name}@{enchant}" if enchant > 0 else name
            expanded.append({
                "item_id": item_id,
                "base_name": name,
                "enchantment": enchant,
                "quality": item["quality"]
            })
    return expanded