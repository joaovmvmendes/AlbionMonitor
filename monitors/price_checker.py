import os
import json
import requests

ITEM_NAME = os.getenv("ITEM_NAME", "T4_BAG")
API_URL = f"https://west.albion-online-data.com/api/v2/stats/prices/{ITEM_NAME}?locations=Bridgewatch&qualities=2"
STATE_FILE = "last_state.json"

def get_api_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Erro ao obter dados da API:", e)
        return []

def load_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_current_state(data):
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f)

def gerar_alertas(data):
    alertas = []

    for item in data:
        item_id = item.get("item_id", "N/A")
        city = item.get("city", "Desconhecida")
        sell_price_min = item.get("sell_price_min", 0)

        print(f"Item: {item_id}, Cidade: {city}, Preço Mínimo: {sell_price_min}")

        if item_id == ITEM_NAME:
            alerta = f"⚠️ O item {item_id} em {city} está com preço mínimo: {sell_price_min}"
            alertas.append(alerta)
            print("Alerta gerado:", alerta)

    return alertas
