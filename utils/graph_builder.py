# utils/graph_builder.py

import matplotlib.pyplot as plt
from datetime import datetime
import os

def gerar_grafico_precos(data, item_id, cidade):
    if not data:
        print(f"[AVISO] Sem dados para o gráfico de {item_id} em {cidade}")
        return None

    try:
        timestamps = [datetime.fromisoformat(d["timestamp"]) for d in data]
        precos = [d["avg_price"] for d in data]

        plt.figure(figsize=(10, 4))
        plt.plot(timestamps, precos, marker="o", linewidth=1.5)
        plt.title(f"📊 Variação de Preço — {item_id} em {cidade}")
        plt.xlabel("Horário")
        plt.ylabel("Preço médio (silver)")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.tight_layout()

        filename = f"graph_{item_id}_{cidade}.png".replace(" ", "_")
        plt.savefig(filename)
        plt.close()

        return filename
    except Exception as e:
        print(f"[ERRO] ao gerar gráfico de {item_id} em {cidade}: {e}")
        return None