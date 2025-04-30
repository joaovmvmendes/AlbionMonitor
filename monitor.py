from monitors.price_checker import get_api_data
from data.data_process import load_last_state, save_current_state
from bot.telegram import send_telegram
from alerts.generate_alerts import gerar_alertas
import os

ITEM_NAMES = os.getenv("ITEM_NAME", "T4_BAG").split(",")
CITIES = os.getenv("CITIES", "Caerleon,Bridgewatch,Thetford,Martlock,Fortsterling,Lymhurst,Brecilien").split(",")

def main():
    all_data = []
    
    for item_name in ITEM_NAMES:
        cities_str = ",".join(CITIES)
        url = f"https://west.albion-online-data.com/api/v2/stats/prices/{item_name}?locations={cities_str}&qualities=2"
        print(f"Buscando dados para: {item_name} nas cidades: {cities_str}")
        data = get_api_data(url)
        all_data.extend(data)

    last_state = load_last_state()
    print("Último estado salvo:", last_state)

    alertas = gerar_alertas(all_data, ITEM_NAMES, agrupamento="city")
    print(f"Alertas gerados: {alertas}")

    if alertas:
        print("Enviando alerta para o Telegram...")
        send_telegram("\n".join(alertas))
    else:
        print("Nenhum alerta gerado.")

    save_current_state(all_data)

if __name__ == "__main__":
    main()
