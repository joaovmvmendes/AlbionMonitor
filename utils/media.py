import os
from notifications.telegram import send_telegram_photo

def send_image_and_cleanup(image_path):
    """
    Sends an image via Telegram and deletes the file after sending.
    """
    if send_telegram_photo(image_path):
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                print(f"⚠️ Erro ao tentar remover a imagem: {e}")