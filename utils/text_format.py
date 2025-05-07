def build_arbitrage_text(index: int, base_name: str, enchantment: int, quality_str: str, opportunity: dict, sales_line: str) -> str:
    """
    Builds a Telegram-formatted message with arbitrage information.

    Parameters:
        index (int): Position in the list.
        base_name (str): Name of the base item.
        enchantment (int): Enchantment level.
        quality_str (str): String label for item quality.
        opportunity (dict): Dictionary containing origin, destination, prices, profit and margin.
        sales_line (str): Additional sales information (e.g., sales volume).

    Returns:
        str: Formatted message for the Telegram bot.
    """
    enchantment_str = f" (Enchanted +{enchantment})" if enchantment else ""
    return (
        f"{index}. *{base_name}{enchantment_str}* — Quality: {quality_str}\n"
        f"Buy in {opportunity.get('origem')} for `{opportunity.get('preco_origem')}`\n"
        f"Sell in {opportunity.get('destino')} for `{opportunity.get('preco_destino')}`\n"
        f"Profit: `{opportunity.get('lucro')}` silver ({opportunity.get('margem', 0):.1%})\n"
        f"{sales_line}\n"
    )