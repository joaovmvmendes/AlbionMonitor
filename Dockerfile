# Usar imagem base com Python
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar arquivos do projeto
COPY requirements.txt .
COPY Monitor.py ./monitor.py
COPY monitors/ monitors/
COPY bot/ bot/

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Rodar o script
CMD ["python", "monitor.py"]
