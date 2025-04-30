from monitors.price_checker import get_api_data
from data.data_process import load_last_state, save_current_state
from bot.telegram import send_telegram
from alerts.generate_alerts import gerar_alertas
import os

ITEM_NAMES = os.getenv("ITEM_NAME", "T4_BAG").split(",")
CITIES = os.getenv("CITIES", "Caerleon,Bridgewatch,Thetford,Martlock,Fortsterling,Lymhurst,Brecilien").split(",")
API_URL_TEMPLATE = "https://west.albion-online-data.com/api/v2/stats/prices/{item_name}?locations={cities}&qualities=2"

def main():
    data = get_api_data(API_URL_TEMPLATE, ITEM_NAME, CITIES)
    print("Dados recebidos da API:", data)

    last_state = load_last_state()
    print("Último estado salvo:", last_state)

    alertas = gerar_alertas(data, ITEM_NAME)
    print(f"Alertas gerados: {alertas}")  # Confirme os alertas gerados

    if alertas:
        print("Enviando alerta para o Telegram...")
        send_telegram("\n".join(alertas))  # Verifique se a mensagem está sendo enviada
    else:
        print("Nenhum alerta gerado.")

    save_current_state(data)
