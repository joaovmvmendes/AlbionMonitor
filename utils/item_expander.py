def expand_item_variants(config_items):
    """
    Expands base items into all combinations of enchantments and quality levels.

    Parameters:
        config_items (list): Each dict must contain 'base_name', 'enchantments', and 'quality'.

    Returns:
        list: List of item variant dictionaries with keys: item_id, base_name, enchantment, quality.
    """
    expanded = []

    for item in config_items:
        base_name = item.get("base_name")
        enchantments = item.get("enchantments", [])
        quality = item.get("quality")

        if not base_name or quality is None:
            print(f"[AVISO] Item inválido encontrado na configuração: {item}")
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