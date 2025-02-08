# Sorun Giderme Kılavuzu

## Sık Karşılaşılan Hatalar

### 1. API Bağlantı Hataları

#### Hata: Connection Refused
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Çözüm:**
1. API endpoint'in doğruluğunu kontrol et
2. Firewall ayarlarını kontrol et
3. API servisinin çalıştığından emin ol

#### Hata: Authentication Failed
```
401 Unauthorized: Invalid API credentials
```

**Çözüm:**
1. API anahtarlarının doğruluğunu kontrol et
2. Environment variables'ı kontrol et
3. API kullanıcısının yetkilerini kontrol et

### 2. Görsel İşleme Hataları

#### Hata: File Too Large
```
ImageProcessingError: Dosya boyutu çok büyük: 12.5MB
```

**Çözüm:**
1. Görseli optimize et
2. `max_file_size_mb` ayarını kontrol et
3. Görsel sıkıştırma kullan

#### Hata: Invalid Image Format
```
ImageProcessingError: Desteklenmeyen dosya türü: .webp
```

**Çözüm:**
1. Desteklenen formatlara dönüştür (jpg, png, gif)
2. `allowed_types` ayarını kontrol et

### 3. Event Sistemi Hataları

#### Hata: Event Handler Not Found
```
EventError: No handler registered for event 'UPLOAD_COMPLETED'
```

**Çözüm:**
1. Event handler'ın kayıtlı olduğunu kontrol et
2. Event isminin doğruluğunu kontrol et
3. Service başlangıç sırasını kontrol et

### 4. Cache Hataları

#### Hata: Redis Connection Failed
```
RedisConnectionError: Error 111 connecting to localhost:6379
```

**Çözüm:**
1. Redis servisinin çalıştığını kontrol et
2. Bağlantı ayarlarını kontrol et
3. Redis port'unu kontrol et

## Logging ve Debug

### Log Seviyelerini Ayarlama
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)
```

### Debug Mode Aktifleştirme
```bash
export DEBUG=1
export LOG_LEVEL=DEBUG
```

## Health Check

### API Health Check
```bash
curl http://localhost:8000/health

# Beklenen çıktı:
{
    "status": "healthy",
    "services": {
        "database": "up",
        "redis": "up",
        "woocommerce": "up"
    }
}
```

### Service Status
```bash
docker-compose ps
docker-compose logs --tail=100 app
```

## Metrik Kontrolleri

### Prometheus Metrics
```bash
curl http://localhost:9090/metrics | grep wolvox
```

### Grafana Dashboard
1. http://localhost:3000 adresine git
2. "WooCommerce Integration" dashboard'ını aç
3. Error rate ve latency metriklerini kontrol et 