import requests
import json
import os
import re

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_URL = "https://west.albion-online-data.com/api/v2/stats/prices/T4_BAG?locations=Bridgewatch&qualities=2"

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

def escape_markdown(text):
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": escape_markdown(message),
        "parse_mode": "MarkdownV2"
    }

    print("BOT_TOKEN:", "set" if BOT_TOKEN else "not set")
    print("CHAT_ID:", CHAT_ID)
    print("Mensagem que será enviada:", message)

    try:
        response = requests.post(url, data=data)
        print("Resposta do Telegram:", response.status_code, response.text)
    except Exception as e:
        print("Erro ao enviar mensagem para o Telegram:", e)

def main():
    data = get_api_data()
    print("Dados recebidos da API:", data)

    last_state = load_last_state()
    print("Último estado salvo:", last_state)

    alertas = []

    for item in data:
        item_id = item.get("item_id", "N/A")
        city = item.get("city", "Desconhecida")
        sell_price_min = item.get("sell_price_min", 0)

        print(f"Item: {item_id}, Cidade: {city}, Preço Mínimo: {sell_price_min}")

        if item_id == "T4_BAG":
            alerta = f"⚠️ O item {item_id} em {city} está com preço mínimo: {sell_price_min}"
            alertas.append(alerta)
            print("Alerta gerado:", alerta)

    if alertas:
        print("Enviando alerta para o Telegram...")
        send_telegram("\n".join(alertas))
    else:
        print("Nenhum alerta gerado.")

    save_current_state(data)

if __name__ == "__main__":
    main()
