import os
import requests
import logging
from config.settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)

def validate_telegram_config() -> bool:
    """
    Checks if Telegram credentials are properly configured.

    Returns:
        bool: True if credentials exist, False otherwise.
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID in .env.")
        return False
    return True

def send_telegram_message(message: str) -> None:
    """
    Sends a Markdown-formatted text message via Telegram.

    Parameters:
        message (str): The message to send.
    """
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
        logger.info("Message sent successfully.")
    except requests.RequestException as e:
        logger.error(f"Failed to send Telegram message: {e}")

def send_telegram_photo(image_path: str, caption: str = None) -> bool:
    """
    Sends a photo to Telegram with an optional caption.

    Parameters:
        image_path (str): Path to the image file.
        caption (str, optional): Optional caption for the photo.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not validate_telegram_config():
        return False

    if not image_path or not os.path.exists(image_path):
        logger.error(f"Invalid or missing image path: {image_path}")
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
            logger.info(f"Image sent successfully: {image_path}")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to send Telegram image: {e}")
            return False