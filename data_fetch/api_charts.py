import requests

def fetch_item_chart_data(item_id, city, quality=1, dias=3):
    """
    Busca histórico de preço médio por hora (últimos N dias) para um item em uma cidade.
    A API não aceita o sufixo de encantamento (@X), portanto removemos se necessário.
    """
    item_base = item_id.split("@")[0]  # Remove encantamento se houver

    url = f"https://west.albion-online-data.com/api/v2/stats/charts/{item_base}"
    params = {
        "locations": city,
        "qualities": quality,
        "time-scale": 1  # 1 = por hora
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        resultado = response.json()

        for entrada in resultado:
            if entrada.get("location") == city and entrada.get("quality") == quality:
                timestamps = entrada["data"]["timestamps"]
                prices = entrada["data"]["prices_avg"]
                if len(timestamps) != len(prices):
                    print(f"[AVISO] Dados inconsistentes para {item_base}@{city}")
                    return []

                return [
                    {"timestamp": ts, "avg_price": price}
                    for ts, price in zip(timestamps[-24 * dias:], prices[-24 * dias:])
                ]

    except Exception as e:
        print(f"[ERRO] charts API: {item_base}@{city}: {e}")

    return []