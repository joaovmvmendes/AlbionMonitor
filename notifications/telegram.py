import os
import requests
import time
import logging
import re
from sqlalchemy import text
from sqlalchemy.orm import Session
from config.settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from services.albion_api import get_item_prices, get_item_history
from config.db_connections import get_db_session

logger = logging.getLogger(__name__)

def validate_telegram_config() -> bool:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID in .env.")
        return False
    return True

def send_telegram_message(message: str) -> None:
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

def handle_price_compra_command(message_text: str):
    try:
        parts = message_text.strip().split(" ", 1)
        if len(parts) < 2:
            send_telegram_message("Por favor, envie o nome do item.")
            return

        _, query = parts
        tokens = query.strip().split()
        name_parts = []
        enchants = []
        qualities = []

        for token in tokens:
            if re.fullmatch(r"\d(,\d)*", token):
                if not enchants:
                    enchants = [int(x) for x in token.split(",")]
                else:
                    qualities = [int(x) for x in token.split(",")]
            else:
                name_parts.append(token)

        translated_name = " ".join(name_parts)

        with get_db_session() as session:
            result = session.execute(text("""
                SELECT item_unique_name FROM item_localizations
                WHERE name ILIKE :name
                LIMIT 1
            """), {"name": translated_name}).fetchone()

            if not result:
                send_telegram_message(f"Item '{translated_name}' não encontrado.")
                return

            base_uniquename = result[0]
            enchants = enchants or [0]
            qualities = qualities or [1]
            responses = []

            for enchant in enchants:
                item_id = f"{base_uniquename}@{enchant}" if enchant > 0 else base_uniquename
                price_data = get_item_prices(item_id)

                for quality in qualities:
                    filtered = [
                        d for d in price_data
                        if d.get("quality") == quality and d.get("sell_price_min", 0) > 0
                    ]
                    if not filtered:
                        responses.append(f"❌ Sem dados para {item_id} qualidade {quality}.")
                        continue

                    best_offer = min(filtered, key=lambda d: d["sell_price_min"])
                    history = get_item_history(item_id)

                    sales_data = [day.get("item_count", 0) for day in history if day.get("item_count", 0) > 0]
                    daily_avg = sum(sales_data) // max(1, len(sales_data))

                    responses.append(
                        f"🧾 {translated_name} (Encantamento {enchant}, Qualidade {quality})\n"
                        f"📍 Melhor cidade: {best_offer['city']}\n"
                        f"💰 Preço: {best_offer['sell_price_min']} silver\n"
                        f"📈 Média diária: {daily_avg} vendas"
                    )

        send_telegram_message("\n\n".join(responses))

    except Exception as e:
        logger.exception("Erro ao processar comando /precoCompra")
        send_telegram_message("Ocorreu um erro ao processar seu pedido.")

def listen_for_commands():
    logger.info("Iniciando escuta de comandos do Telegram...")
    last_update_id = None

    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            params = {
                "timeout": 30,
                "offset": last_update_id + 1 if last_update_id else None
            }

            response = requests.get(url, params=params, timeout=35)
            response.raise_for_status()
            updates = response.json().get("result", [])

            for update in updates:
                last_update_id = update["update_id"]
                message = update.get("message")
                if not message or "text" not in message:
                    continue

                text = message["text"].strip()
                logger.info(f"Comando recebido: {text}")

                if text.startswith("/precoCompra"):
                    handle_price_compra_command(text)
                else:
                    send_telegram_message("Comando não reconhecido. Use /precoCompra.")

        except Exception as e:
            logger.error(f"Erro ao buscar comandos do Telegram: {e}")
            time.sleep(5)

if __name__ == "__main__":
    listen_for_commands()