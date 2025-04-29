import requests
import json
import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_URL = "https://west.albion-online-data.com/api/v2/stats/prices/T4_BAG?locations=Caerleon,Bridgewatch&qualities=2"

STATE_FILE = "last_state.json"

def get_api_data():
    response = requests.get(API_URL)
    return response.json()

def load_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_current_state(data):
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

def main():
    data = get_api_data()
    last_state = load_last_state()
    alertas = []

    for item in data:
        item_id = item.get("item_id", "N/A")
        city = item.get("city", "Desconhecida")
        sell_price_min = item.get("sell_price_min", 0)

        if item_id = T4_BAG:
            alertas.append(f"⚠️ O item {item_id} em {city} está com preço mínimo: {sell_price_min}")

    if alertas:
        send_telegram("\n".join(alertas))

    save_current_state(data)

if __name__ == "__main__":
    main()
