import requests

def get_api_data(API_URL_TEMPLATE, ITEM_NAME, CITIES):
    print(f"Buscando dados da API com a URL: {API_URL_TEMPLATE}")  # Verifique a URL
    try:
        response = requests.get(API_URL_TEMPLATE)
        response.raise_for_status()
        data = response.json()
        print(f"Dados recebidos da API: {data}")  # Verifique os dados
        return data
    except Exception as e:
        print("Erro ao obter dados da API:", e)
        return []
