# Usar imagem base com Python
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar arquivos do projeto
COPY requirements.txt .
COPY monitor.py ./monitor.py
COPY monitors/ monitors/
COPY bot/ bot/
COPY alerts/ alerts/
COPY data/ data/

# Instalar dependências do sistema
RUN apt update && apt install -y make git gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Rodar o script
CMD ["python", "monitor.py"]
