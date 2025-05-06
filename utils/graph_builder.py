import matplotlib.pyplot as plt
from datetime import datetime
import os

def generate_price_chart(data, item_id, city):
    if not data:
        print(f"[AVISO] Sem dados para o gráfico de {item_id} em {city}")
        return None

    try:
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

        filename = f"graph_{item_id}_{city}.png".replace(" ", "_")
        plt.savefig(filename)
        plt.close()

        return filename
    except Exception as e:
        print(f"[ERRO] ao gerar gráfico de {item_id} em {city}: {e}")
        return None