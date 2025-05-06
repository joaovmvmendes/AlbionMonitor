import requests

def fetch_item_history(item_id, city, dias=7):
    url = f"https://west.albion-online-data.com/api/v2/stats/history/{item_id}.json"
    params = {"locations": city, "time-scale": 24, "qualities": "1,2,3,4,5"}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()[:dias]
    except Exception as e:
        print(f"[ERRO] API histórico {item_id}@{city}: {e}")
        return []