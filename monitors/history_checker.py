import requests

def get_history_data(item, city, dias=7, qualidade=2):
    url = (
        f"https://west.albion-online-data.com/api/v2/stats/history/{item}.json"
        f"?locations={city}&qualities={qualidade}&time-scale=24"
    )
    print(f"Buscando histórico de {item} em {city} (últimos {dias} dias)...")

    try:
        resp = requests.get(url)
        resp.raise_for_status()
        dados = resp.json()
        return dados[:dias]
    except Exception as e:
        print(f"Erro ao buscar histórico de {item} em {city}: {e}")
        return []
