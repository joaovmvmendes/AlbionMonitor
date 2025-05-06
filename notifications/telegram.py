import os
import requests
from config.settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def validate_telegram_config():
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID não configurado no .env.")
        return False
    return True

def send_telegram_message(message):
    """Sends a formatted text message via Telegram using Markdown."""
    if not validate_telegram_config():
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        print("✅ Mensagem enviada com sucesso!")
    except requests.RequestException as e:
        print(f"❌ Erro ao enviar mensagem: {e}")

def send_telegram_photo(image_path, caption=None):
    """Sends a photo to Telegram with an optional caption."""
    if not validate_telegram_config():
        return False

    if not image_path or not os.path.exists(image_path):
        print(f"❌ Caminho da imagem inválido ou inexistente: {image_path}")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(image_path, "rb") as photo:
        files = {"photo": photo}
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": caption,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, data=data, files=files, timeout=10)
            response.raise_for_status()
            print(f"✅ Imagem enviada com sucesso: {image_path}")
            return True
        except Exception as e:
            print(f"❌ Erro ao enviar imagem: {e}")
            return False