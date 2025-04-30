import requests

def get_api_data(api_url_template: str, item_names: list[str], cities: list[str]):
    item_query = ",".join(item_names)
    city_query = ",".join(cities)
    api_url = api_url_template.format(item_names=item_query, cities=city_query)

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Erro ao obter dados da API:", e)
        return []
