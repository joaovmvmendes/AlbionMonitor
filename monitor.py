from monitors.price_checker import get_api_data, load_last_state, save_current_state, gerar_alertas
from bot.telegram import send_telegram
from monitors.price_checker import pri

def main():
    data = get_api_data()
    print("Dados recebidos da API:", data)

    last_state = load_last_state()
    print("Último estado salvo:", last_state)

    alertas = gerar_alertas(data)

    if alertas:
        print("Enviando alerta para o Telegram...")
        send_telegram("\n".join(alertas))
    else:
        print("Nenhum alerta gerado.")

    save_current_state(data)

if __name__ == "__main__":
    main()
