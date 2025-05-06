import matplotlib.pyplot as plt
from datetime import datetime
import os

def generate_price_chart(data, item_id, city, output_dir="charts"):
    """
    Generates and saves a price chart image from timestamped data.

    Parameters:
        data (list): List of dicts with keys 'timestamp' and 'avg_price'.
        item_id (str): Item identifier.
        city (str): City name.
        output_dir (str): Directory where image will be saved.

    Returns:
        str or None: Path to the saved image, or None on failure.
    """
    if not data:
        print(f"[AVISO] Sem dados para o gráfico de {item_id} em {city}")
        return None

    try:
        os.makedirs(output_dir, exist_ok=True)
        timestamps = [datetime.fromisoformat(entry["timestamp"]) for entry in data]
        prices = [entry["avg_price"] for entry in data]

        plt.figure(figsize=(10, 4))
        plt.plot(timestamps, prices, marker="o", linewidth=1.5)
        plt.title(f"📊 Variação de Preço — {item_id} em {city}")
        plt.xlabel("Horário")
        plt.ylabel("Preço médio (silver)")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.tight_layout()

        filename = f"{item_id}_{city}.png".replace(" ", "_")
        path = os.path.join(output_dir, filename)

        plt.savefig(path)
        plt.close()

        return path

    except Exception as e:
        print(f"[ERRO] ao gerar gráfico de {item_id} em {city}: {e}")
        return None