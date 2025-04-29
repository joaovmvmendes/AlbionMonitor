import requests
import json
import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_URL = "https://api.suaapi.com/dados"

STATE_FILE = "last_state.json"

def get_api_data():
    response = requests.get(API_URL)
    return response.json()

def load_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

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

    # Exemplo de análise
    preco = data.get("preco", 0)
    volume = data.get("volume", 0)

    alertas = []

    if preco > 12:
        alertas.append(f"⚠️ Preço acima do limite: {preco}")
    if volume < 90:
        alertas.append(f"📉 Volume muito baixo: {volume}")

    if alertas:
        send_telegram("\n".join(alertas))

    save_current_state(data)

if __name__ == "__main__":
    main()
