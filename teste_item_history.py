import requests

def testar_item_history(item_id="T4_BAG", city="Martlock", quality="1", dias=7):
    url = f"https://west.albion-online-data.com/api/v2/stats/history/{item_id}.json"
    params = {
        "locations": city,
        "qualities": quality,
        "time-scale": 24
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        dados = resp.json()[:dias]

        if not dados:
            print(f"[!] Nenhum dado retornado para {item_id} em {city}")
            return

        for dia in dados:
            print("→ Registro bruto recebido:", dia)
            data = dia.get('timestamp', 'sem data')
            item_count = dia.get('item_count', 'N/A')
            preco_medio = dia.get('prices_avg', 'N/A')
            print(f"{data} - vendas: {item_count} - preço médio: {preco_medio}")

    except Exception as e:
        print(f"[ERRO] Falha na requisição: {e}")

# Chamando a função (isso deve estar sem espaços antes)
testar_item_history()