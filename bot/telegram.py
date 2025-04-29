import os
import re
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def escape_markdown(text):
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)

def send_telegram(message: str):
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
