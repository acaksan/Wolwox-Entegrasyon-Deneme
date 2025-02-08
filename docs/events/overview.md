# Event Sistemi

## Genel Bakış

Event sistemi, WooCommerce ve Wolvox arasındaki senkronizasyonu ve iletişimi yönetir. Asenkron yapıda çalışan bu sistem, servisler arası iletişimi ve veri tutarlılığını sağlar.

## Özellikler

- Asenkron event yayınlama ve dinleme
- Event geçmişi ve loglama
- Otomatik retry mekanizması
- Hata yönetimi ve izleme
- Event filtreleme ve routing

## Temel Kullanım

```python
# Event Service oluşturma
event_service = EventService()

# Event yayınlama
await event_service.publish("product_updated", {
    "product_id": 123,
    "changes": {"stock": 10},
    "timestamp": datetime.now().isoformat()
})

# Event dinleme
@event_handler("product_updated")
async def handle_product_update(data: Dict):
    product_id = data["product_id"]
    changes = data["changes"]
    await sync_service.sync_product(product_id)
```

## Event Yapısı

Her event şu bilgileri içerir:

```python
{
    "type": "event_type",        # Event tipi
    "data": {},                  # Event verileri
    "timestamp": "",             # Oluşturulma zamanı
    "id": "uuid",               # Unique ID
    "status": "success/failed"   # Event durumu
}
```

## Hata Yönetimi

```python
try:
    await event_service.publish("order_created", order_data)
except EventPublishError as e:
    logger.error(f"Event yayınlama hatası: {str(e)}")
    # Retry mekanizması devreye girer
```

## Event Geçmişi

```python
# Son eventleri getir
events = await event_service.get_event_history()

# Belirli tipteki eventleri filtrele
product_events = await event_service.get_event_history(
    event_type="product_updated"
)
```

## Event Tipleri

### Product Events
- product_created
- product_updated
- product_deleted
- stock_changed
- price_changed

### Order Events
- order_created
- order_status_changed
- order_completed
- order_cancelled
- order_refunded

## Metrik Events

### Sistem Metrikleri
- CPU kullanımı
- RAM kullanımı
- Disk kullanımı
- Bağlantı havuzu durumu

### Servis Events
- Servis başlatma/kapatma
- API istekleri
- Cache operasyonları
- Hata durumları

## Lifecycle Events

### Startup Events
```python
async def startup_event():
    # Servisleri başlat
    app_state['woo_service'] = WooCommerceService()
    app_state['media_service'] = WooCommerceMediaService()
    
    # Metrikleri başlat
    await update_system_metrics()
    await update_system_info()
```

### Shutdown Events
```python
async def shutdown_event():
    # Servisleri temizle
    if 'woo_service' in app_state:
        await app_state['woo_service'].close()
    if 'media_service' in app_state:
        await app_state['media_service'].close()
```

## Periyodik Tasks

### Metrik Güncelleme
```python
async def periodic_metrics_update():
    while True:
        await update_system_metrics()
        await asyncio.sleep(60)  # Her dakika
``` 