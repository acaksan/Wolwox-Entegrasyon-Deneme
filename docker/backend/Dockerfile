# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Gerekli paketleri kopyala
COPY backend/requirements.txt .

# Sanal ortam oluştur ve bağımlılıkları yükle
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim

# Firebird client kurulumu
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    firebird3.0-utils && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

# Uygulama kodlarını kopyala
COPY backend/src .

# Python path'i ayarla
ENV PYTHONPATH=/app
ENV PATH="/opt/venv/bin:$PATH"

# Uvicorn için port
EXPOSE 8000

# Uygulamayı başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 