import requests

def get_api_data(url):
    print(f"Buscando dados da API na URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"Dados recebidos: {len(data)} itens")
        return data
    except Exception as e:
        print("Erro ao obter dados da API:", e)
        return []
