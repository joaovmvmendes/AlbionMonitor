import os
import re
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage"
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    # Verifique se a URL e os dados estão corretos
    print(f"Enviando mensagem para o Telegram: {message}")
    
    params = {
        'chat_id': chat_id,
        'text': message
    }
    
    try:
        response = requests.post(TELEGRAM_API_URL, data=params)
        response.raise_for_status()
        print("Mensagem enviada com sucesso!")  # Confirme que a resposta foi bem-sucedida
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem para o Telegram: {e}")
