# 📁 config/settings.py
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env (apenas em ambiente local)
if os.path.exists(".env"):
    load_dotenv()

# ⬆️ Margens de lucro para os filtros de arbitragem
MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.15))
MAX_PROFIT_MARGIN = float(os.getenv("MAX_PROFIT_MARGIN", 10))

# 📢 Configuração do Bot do Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 📂 Arquivo local para salvar estado do bot
STATE_FILE_PATH = "last_state.json"