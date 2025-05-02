import psycopg2
from utils.db import get_connection

# Dados auxiliares com base na wiki oficial
CATEGORIES = ["armor", "weapon", "accessory", "consumable", "tool", "mount", "artefact"]
ITEM_TYPES = ["melee", "ranged", "magic", "offhand", "bag", "gathering", "token", "farmable"]
SUBTYPES = ["plate", "leather", "cloth", "sword", "axe", "bow", "mace", "hammer", "staff", "shield"]
RARITIES = ["common", "uncommon", "rare", "epic", "legendary", "artifact"]

def popular_tabela(tabela, valores):
    conn = get_connection()
    cur = conn.cursor()
    print(f"✨ Populando tabela: {tabela}...")
    for valor in valores:
        cur.execute(f"""
            INSERT INTO {tabela} (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
        """, (valor,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Tabela '{tabela}' populada com sucesso!\n")

if __name__ == "__main__":
    popular_tabela("categories", CATEGORIES)
    popular_tabela("item_types", ITEM_TYPES)
    popular_tabela("subtypes", SUBTYPES)
    popular_tabela("rarities", RARITIES)
