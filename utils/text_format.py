def build_arbitrage_text(index, base_name, enchantment, quality_str, opportunity, sales_line):
    enchantment_str = f" (Encantado +{enchantment})" if enchantment else ""
    return (
        f"{index}. *{base_name}{enchantment_str}* — Qualidade: {quality_str}\n"
        f"Comprar em {opportunity['origem']} por `{opportunity['preco_origem']}`\n"
        f"Vender em {opportunity['destino']} por `{opportunity['preco_destino']}`\n"
        f"Lucro: `{opportunity['lucro']}` silver ({opportunity['margem']:.1%})\n"
        f"{sales_line}\n"
    )