import time
import requests

API_BASE = "https://west.albion-online-data.com/api/v2/stats/prices"
CIDADES = [
    "Caerleon", "Bridgewatch", "Lymhurst",
    "Martlock", "Fort Sterling", "Thetford", "Brecilien"
]

LUCRO_MAXIMO = 10.0  # 1000%
precos_cache = {}

def get_item_prices_from_api(item_id, qualidade=None):
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
