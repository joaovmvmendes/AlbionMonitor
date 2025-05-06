import time
import requests
from config.constants import API_BASE_URL, CITIES

API_BASE = API_BASE_URL
precos_cache = {}

def get_item_prices_from_api(item_id, qualidade=None):
    chave = f"{item_id}|{qualidade or 'any'}"
    if chave in precos_cache:
        return precos_cache[chave]

    print(f"🔍 Buscando preços para: {item_id}" + (f" (Qualidade {qualidade})" if qualidade else ""))
    params = {"locations": ",".join(CITIES)}
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