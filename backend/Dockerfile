# Backend Dockerfile

# Python base image
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# PYTHONPATH ayarı
ENV PYTHONPATH=/app

# Port ayarı
EXPOSE 8000

# Uygulamayı başlat
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
