import os
import logging
from notifications.telegram import send_telegram_photo

logger = logging.getLogger(__name__)

def send_image_and_cleanup(image_path: str) -> None:
    """
    Sends an image to Telegram and deletes it afterward to free disk space.

    Parameters:
        image_path (str): Full path to the image to be sent.
    """
    if send_telegram_photo(image_path):
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
                logger.debug(f"Image file removed after sending: {image_path}")
            except Exception as e:
                logger.warning(f"Failed to remove image file: {image_path} - {e}")