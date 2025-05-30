# Base image with Python
FROM python:3.11-slim

# Set working directory
WORKDIR /AlbionMonitor

# Copy project files
COPY . .

# Set environment variables (avoid .pyc, set UTF-8)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Default command
CMD ["python", "AlbionMonitor/main.py"]