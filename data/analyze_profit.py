import time
import requests
from utils.db import get_connection

API_BASE = "https://west.albion-online-data.com/api/v2/stats/prices"
CIDADES = [
    "Caerleon", "Bridgewatch", "Lymhurst",
    "Martlock", "Fort Sterling", "Thetford", "Brecilien"
]
LUCRO_MAXIMO = 10.0  # 1000%

precos_cache = {}

def buscar_preco_item(item_id, qualidade=None):
    chave = f"{item_id}|{qualidade or 'any'}"
    if chave in precos_cache:
        return precos_cache[chave]

    print(f"🔍 Buscando preços para: {item_id}" + (f" (Qualidade {qualidade})" if qualidade else ""))
    params = {"locations": ",".join(CIDADES)}
    if qualidade:
        params["qualities"] = qualidade

    try:
        resp = requests.get(f"{API_BASE}/{item_id}.json", params=params, timeout=10)
        resp.raise_for_status()
        dados = resp.json()
        precos_cache[chave] = dados
        time.sleep(0.35)
        return dados
    except Exception as e:
        print(f"⚠️ Erro ao buscar preço para {item_id}: {e}")
        return []

def obter_unique_name(nome, enchantment):
    conn = get_connection()
    cur = conn.cursor()
    nome = nome.strip().lower()

    cur.execute("""
        SELECT i.unique_name
        FROM items i
        JOIN item_localizations l ON i.unique_name = l.item_id
        WHERE (LOWER(l.name) = %s OR LOWER(i.unique_name) = %s)
        AND i.enchantment_level = %s
        ORDER BY i.tier DESC
        LIMIT 1
    """, (nome, nome, str(enchantment)))

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None

def obter_recursos_para_item(item_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT resource_id, quantity
        FROM craft_resources
        WHERE item_id = %s
    """, (item_id,))
    recursos = cur.fetchall()
    cur.close()
    conn.close()
    return recursos

def analisar_lucro(nome_item, enchantment, qualidade):
    item_id = obter_unique_name(nome_item, enchantment)
    if not item_id:
        print(f"❌ Item '{nome_item}' com enchantment {enchantment} não encontrado.")
        return

    precos_venda = buscar_preco_item(item_id, qualidade)
    venda_por_cidade = {
        p['city']: p.get('sell_price_min', 0)
        for p in precos_venda if p.get('sell_price_min', 0) > 0
    }
    if not venda_por_cidade:
        print("❌ Nenhuma cidade com preço de venda disponível.")
        return

    recursos = obter_recursos_para_item(item_id)
    if not recursos:
        print("❌ Nenhum recurso de crafting encontrado.")
        return

    custo_total = 0
    compras = {}

    for recurso_id, qtd in recursos:
        recurso_enchanted = f"{recurso_id}@{enchantment}" if enchantment > 0 else recurso_id
        precos_recurso = buscar_preco_item(recurso_enchanted)

        menor_preco = float('inf')
        melhor_cidade = None
        for p in precos_recurso:
            preco = p.get("sell_price_min", 0)
            if preco > 0 and preco < menor_preco:
                menor_preco = preco
                melhor_cidade = p['city']

        if menor_preco == float('inf'):
            print(f"⚠️ Recurso {recurso_enchanted} sem preço disponível.")
            return

        custo_total += menor_preco * qtd
        compras[recurso_enchanted] = (qtd, melhor_cidade, menor_preco)

    melhor_lucro = None
    for cidade, preco_venda in venda_por_cidade.items():
        lucro = preco_venda - custo_total
        margem = lucro / custo_total
        if 0 < margem <= LUCRO_MAXIMO:
            if not melhor_lucro or margem > melhor_lucro['margem']:
                melhor_lucro = {
                    "cidade": cidade,
                    "preco": preco_venda,
                    "lucro": lucro,
                    "margem": round(margem * 100, 2)
                }

    print("\n============================")
    print(f"Item: {item_id} | Enchant: {enchantment} | Qualidade: {qualidade}")
    print("\n📦 Recursos necessários:")
    for recurso, (qtd, cidade, preco) in compras.items():
        print(f"  - {qtd}x {recurso} em {cidade} por {preco:.2f} cada")

    print("\n💰 Melhor venda:")
    if melhor_lucro:
        print(f"  - Cidade: {melhor_lucro['cidade']}")
        print(f"  - Venda por: {melhor_lucro['preco']:.2f}")
        print(f"  - Lucro: {melhor_lucro['lucro']:.2f}")
        print(f"  - Margem: {melhor_lucro['margem']}%")
    else:
        print("  ❌ Nenhuma cidade com lucro adequado.")

if __name__ == "__main__":
    nome = input("🔎 Nome do item (PT-BR ou EN): ").strip()
    enchant = int(input("✨ Enchantment (0-4): ").strip())
    qualidade = int(input("⭐ Qualidade do item (1-5): ").strip())
    analisar_lucro(nome, enchant, qualidade)