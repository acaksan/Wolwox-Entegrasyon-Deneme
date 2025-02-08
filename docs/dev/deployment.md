# Deployment Rehberi

## Gereksinimler

### Sistem Gereksinimleri
- Python 3.8+
- Redis 6+
- RabbitMQ 3.8+
- Firebird 3.0+

### Python Paketleri
```bash
pip install -r requirements.txt
```

## Ortam Değişkenleri

`.env` dosyası örneği:
```env
# WooCommerce
WOOCOMMERCE_URL=https://your-store.com
WOOCOMMERCE_KEY=your_consumer_key
WOOCOMMERCE_SECRET=your_consumer_secret

# Wolvox (Firebird)
WOLVOX_DB_HOST=localhost
WOLVOX_DB_PORT=3050
WOLVOX_DB_NAME=/path/to/database.fdb
WOLVOX_DB_USER=SYSDBA
WOLVOX_DB_PASSWORD=masterkey

# Redis Cache
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
```

## Docker ile Deployment

### Docker Compose
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    volumes:
      - ./logs:/app/logs
    depends_on:
      - redis
      - rabbitmq
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  rabbitmq:
    image: rabbitmq:3.8-management
    ports:
      - "5672:5672"
      - "15672:15672"
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    restart: unless-stopped

volumes:
  redis_data:
  rabbitmq_data:
```

## Deployment Adımları

1. **Ortamı Hazırlama**
```bash
# Gerekli dizinleri oluştur
mkdir -p logs data

# Env dosyasını kopyala ve düzenle
cp .env.example .env
nano .env
```

2. **Docker ile Deployment**
```bash
# Docker imajını oluştur
docker-compose build

# Servisleri başlat
docker-compose up -d

# Logları izle
docker-compose logs -f
```

3. **Manuel Deployment**
```bash
# Uygulamayı başlat
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4

# Worker'ı başlat
python -m src.worker
```

## Monitoring

### Sağlık Kontrolleri
```bash
# API sağlık kontrolü
curl http://localhost:8000/health

# Redis kontrolü
redis-cli ping

# RabbitMQ kontrolü
rabbitmqctl status
```

### Log Yönetimi
```bash
# Log rotasyonu
logrotate /etc/logrotate.d/woocommerce-wolvox

# Log analizi
tail -f logs/app.log | grep ERROR
```

## Backup ve Recovery

### Redis Backup
```bash
# Anlık backup
redis-cli save

# Otomatik backup (redis.conf)
save 900 1
save 300 10
save 60 10000
```

### RabbitMQ Backup
```bash
# Tanımları yedekle
rabbitmqctl export_definitions definitions.json

# Geri yükle
rabbitmqctl import_definitions definitions.json
```

## Güvenlik Önlemleri

1. **Firewall Kuralları**
```bash
# Redis
ufw allow from 172.16.0.0/12 to any port 6379

# RabbitMQ
ufw allow from 172.16.0.0/12 to any port 5672
ufw allow from trusted_ip to any port 15672
```

2. **SSL/TLS Yapılandırması**
- API için SSL sertifikası
- RabbitMQ için SSL yapılandırması
- Redis şifreleme

3. **Erişim Kontrolleri**
- API authentication
- RabbitMQ kullanıcı yönetimi
- Redis şifre koruması

## CI/CD Pipeline

GitHub Actions workflow örneği:
```yaml
name: CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          make test
          make coverage

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
``` 