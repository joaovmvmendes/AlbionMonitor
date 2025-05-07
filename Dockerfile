# Base image with Python 3.11 (slim variant)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install testing tools
RUN pip install --no-cache-dir pytest coverage black flake8

# Install system dependencies (gcc required for some packages)
RUN apt update && apt install -y gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy application source code
COPY main.py .
COPY config/ config/
COPY monitors/ monitors/
COPY notifications/ notifications/
COPY services/ services/
COPY utils/ utils/
COPY data/ data/
COPY tests/ tests/

# Default command: runs main monitor
CMD ["python", "main.py"]