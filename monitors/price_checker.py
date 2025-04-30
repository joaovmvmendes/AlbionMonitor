import requests
import os

ITEM_NAME = os.getenv("ITEM_NAME", "T4_BAG")
API_URL = f"https://west.albion-online-data.com/api/v2/stats/prices/{ITEM_NAME}?locations=Bridgewatch&qualities=2"

def get_api_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Erro ao obter dados da API:", e)
        return []