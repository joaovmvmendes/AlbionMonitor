# config/settings.py
import os
from dotenv import load_dotenv

# Carrega o .env localmente se existir
if os.path.exists(".env"):
    load_dotenv()

# Configurações de margem e Telegram (funciona com .env ou GitHub Secrets)
MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.15))
MAX_PROFIT_MARGIN = float(os.getenv("MAX_PROFIT_MARGIN", 10))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Caminho do arquivo de estado
STATE_FILE_PATH = "last_state.json"
