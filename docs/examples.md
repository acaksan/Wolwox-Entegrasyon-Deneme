# Örnek Kullanım Senaryoları

## 1. Ürün Senkronizasyonu

### Yeni Ürün Ekleme
```python
from src.services import WooCommerceProductService

async def add_new_product():
    product_service = WooCommerceProductService()
    
    product_data = {
        "name": "Test Ürün",
        "sku": "TST001",
        "regular_price": "99.90",
        "stock_quantity": 100
    }
    
    result = await product_service.create_product(product_data)
    print(f"Ürün oluşturuldu: {result['id']}")
```

### Stok Güncelleme
```python
async def update_stock():
    product_service = WooCommerceProductService()
    
    updates = [
        {"sku": "TST001", "stock_quantity": 50},
        {"sku": "TST002", "stock_quantity": 75}
    ]
    
    results = await product_service.bulk_update_stock(updates)
    print(f"{len(results)} ürün güncellendi")
```

## 2. Sipariş İşlemleri

### Yeni Siparişleri İzleme
```python
from src.services import WooCommerceOrderService, EventService

async def handle_new_order(order_data: dict):
    print(f"Yeni sipariş alındı: {order_data['id']}")
    # Wolvox'a aktar
    
async def setup_order_listener():
    event_service = EventService()
    await event_service.subscribe("order_created", handle_new_order)
```

### Sipariş Durumu Güncelleme
```python
async def update_order_status(order_id: int, status: str):
    order_service = WooCommerceOrderService()
    
    result = await order_service.update_order_status(
        order_id,
        status
    )
    print(f"Sipariş durumu güncellendi: {result['status']}")
```

## 3. Webhook Yönetimi

### Webhook Oluşturma
```python
from src.services import WooCommerceWebhookService

async def setup_webhooks():
    webhook_service = WooCommerceWebhookService()
    
    webhooks = [
        {
            "name": "Yeni Sipariş",
            "topic": "order.created",
            "delivery_url": "https://api.example.com/webhooks/order"
        },
        {
            "name": "Stok Değişimi",
            "topic": "product.updated",
            "delivery_url": "https://api.example.com/webhooks/stock"
        }
    ]
    
    for webhook in webhooks:
        result = await webhook_service.create_webhook(webhook)
        print(f"Webhook oluşturuldu: {result['id']}")
```

## 4. Cache Kullanımı

### Ürün Cache Örneği
```python
from src.core.cache import cached

class ProductService:
    @cached(ttl=300)  # 5 dakika cache
    async def get_product(self, product_id: int):
        # Ürün bilgilerini getir
        return product
        
    async def invalidate_cache(self, product_id: int):
        cache = AsyncCache()
        await cache.delete(f"product:{product_id}")
```

## 5. Batch İşlemler

### Toplu Ürün Güncelleme
```python
async def bulk_update_products():
    product_service = WooCommerceProductService()
    
    updates = [
        {
            "sku": "TST001",
            "regular_price": "89.90",
            "sale_price": "79.90"
        },
        {
            "sku": "TST002",
            "regular_price": "149.90",
            "stock_quantity": 25
        }
    ]
    
    results = await product_service.bulk_update_products(updates)
    print(f"{len(results)} ürün güncellendi")
```

## 6. Raporlama

### Satış Raporu
```python
from src.services import ReportService

async def generate_sales_report(start_date: str, end_date: str):
    report_service = ReportService()
    
    report = await report_service.get_sales_report(
        start_date=start_date,
        end_date=end_date,
        group_by="day"
    )
    
    print(f"Toplam Satış: {report['total_sales']}")
    print(f"Sipariş Sayısı: {report['total_orders']}")
```

# Örnek Kullanımlar

## 1. Görsel Yükleme

```python
from src.services import WooCommerceMediaService

async def upload_product_image():
    service = WooCommerceMediaService()
    
    # Basit yükleme
    result = await service.upload_image(
        file_path="product.jpg",
        title="Ürün Görseli"
    )
    
    # SEO bilgileri ile
    result = await service.upload_image(
        file_path="product.jpg",
        title="Ürün Görseli",
        alt_text="Ürün detay görseli",
        caption="Ürün ön görünüm"
    )
    
    # Batch yükleme
    results = await service.bulk_upload_images([
        "product1.jpg",
        "product2.jpg",
        "product3.jpg"
    ])
```

## 2. Event Handling

```python
from src.services import EventService
from src.core.decorators import event_handler

# Event publish
await event_service.publish(
    "UPLOAD_COMPLETED",
    {"file_id": "123", "status": "success"}
)

# Event subscribe
@event_handler("UPLOAD_COMPLETED")
async def handle_upload(data):
    product_id = data["product_id"]
    await update_product(product_id)
```

## 3. Error Handling

```python
from src.core.exceptions import ServiceException

try:
    result = await service.process_image("large.jpg")
except ServiceException as e:
    logger.error(f"İşlem hatası: {str(e)}")
    if e.details:
        logger.error(f"Detaylar: {e.details}")
```

## 4. Rate Limiting

```python
from src.core.decorators import rate_limit

@rate_limit(calls=100, period=60)
async def api_call():
    return await make_request()
``` 