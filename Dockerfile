# Usar imagem base com Python
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar arquivos necessários
COPY requirements.txt ./
COPY monitor.py ./
COPY .env ./

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Rodar o script
CMD ["python", "monitor.py"]
