# Performance Optimizasyon Rehberi

## 1. Database Optimizasyonları

### Connection Pooling
```python
from src.core.db import DatabasePool

class Database:
    def __init__(self):
        self.pool = DatabasePool(
            min_size=5,
            max_size=20,
            max_queries=50000,
            timeout=60
        )
    
    async def get_connection(self):
        async with self.pool.acquire() as conn:
            return conn
```

### Query Optimizasyonu
```python
# N+1 probleminden kaçın
# Kötü örnek:
async def get_orders_with_items():
    orders = await db.fetch_all("SELECT * FROM orders")
    for order in orders:
        items = await db.fetch_all(
            "SELECT * FROM items WHERE order_id = ?",
            order['id']
        )
        order['items'] = items

# İyi örnek:
async def get_orders_with_items():
    return await db.fetch_all("""
        SELECT o.*, i.*
        FROM orders o
        LEFT JOIN items i ON i.order_id = o.id
    """)
```

### Bulk Operations
```python
async def bulk_update_stock(updates: List[Dict]):
    query = """
        UPDATE products 
        SET stock_quantity = ?
        WHERE sku = ?
    """
    
    async with db.transaction():
        await db.executemany(
            query,
            [(u['quantity'], u['sku']) for u in updates]
        )
```

## 2. Caching Stratejileri

### Multi-Level Caching
```python
class CacheManager:
    def __init__(self):
        self.memory_cache = {}  # L1 cache
        self.redis = AsyncCache()  # L2 cache
    
    async def get(self, key: str):
        # Önce memory cache'e bak
        if key in self.memory_cache:
            return self.memory_cache[key]
            
        # Redis'e bak
        value = await self.redis.get(key)
        if value:
            self.memory_cache[key] = value
            
        return value
```

### Cache Patterns
```python
# Cache-Aside Pattern
async def get_product(id: int):
    cache_key = f"product:{id}"
    
    # Cache'den kontrol et
    product = await cache.get(cache_key)
    if product:
        return product
        
    # DB'den al ve cache'e kaydet
    product = await db.fetch_one(
        "SELECT * FROM products WHERE id = ?",
        id
    )
    await cache.set(cache_key, product, ttl=300)
    return product

# Write-Through Pattern
async def update_product(id: int, data: dict):
    # Önce DB'yi güncelle
    await db.execute(
        "UPDATE products SET ? WHERE id = ?",
        data, id
    )
    
    # Sonra cache'i güncelle
    cache_key = f"product:{id}"
    await cache.set(cache_key, {**data, 'id': id})
```

## 3. API Optimizasyonları

### Response Compression
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000  # 1KB'dan büyük responselar için
)
```

### Pagination ve Filtering
```python
async def get_products(
    page: int = 1,
    per_page: int = 20,
    filters: dict = None
):
    query = "SELECT * FROM products"
    params = []
    
    if filters:
        conditions = []
        for key, value in filters.items():
            conditions.append(f"{key} = ?")
            params.append(value)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
    
    # Pagination
    offset = (page - 1) * per_page
    query += f" LIMIT {per_page} OFFSET {offset}"
    
    return await db.fetch_all(query, *params)
```

## 4. Asenkron Optimizasyonları

### Task Batching
```python
async def sync_products(product_ids: List[int]):
    # Tasks oluştur
    tasks = [
        sync_product(id)
        for id in product_ids
    ]
    
    # Chunk'lara böl ve çalıştır
    chunk_size = 10
    for i in range(0, len(tasks), chunk_size):
        chunk = tasks[i:i + chunk_size]
        await asyncio.gather(*chunk)
```

### Background Tasks
```python
from fastapi import BackgroundTasks

@app.post("/orders")
async def create_order(
    order: OrderCreate,
    background_tasks: BackgroundTasks
):
    # Siparişi kaydet
    order_id = await db.create_order(order)
    
    # Background task'ları ekle
    background_tasks.add_task(send_order_email, order_id)
    background_tasks.add_task(update_inventory, order.items)
    
    return {"order_id": order_id}
```

## 5. Memory Optimizasyonları

### Object Pooling
```python
class ObjectPool:
    def __init__(self, factory, size: int = 10):
        self.factory = factory
        self.objects = [factory() for _ in range(size)]
        
    async def acquire(self):
        if not self.objects:
            return self.factory()
        return self.objects.pop()
        
    async def release(self, obj):
        self.objects.append(obj)
```

### Memory Profiling
```python
from memory_profiler import profile

@profile
async def memory_intensive_task():
    data = []
    for i in range(1000000):
        data.append({"id": i})
    return data
```

## 6. Monitoring

### Performance Metrics
```python
from prometheus_client import Histogram

REQUEST_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

@app.middleware("http")
async def track_performance(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_LATENCY.labels(
        endpoint=request.url.path
    ).observe(duration)
    
    return response
```

## 7. Performance Checklist

### Development
- [ ] Query planları analiz edildi mi?
- [ ] N+1 sorguları kontrol edildi mi?
- [ ] Cache stratejisi belirlendi mi?
- [ ] Bulk operasyonlar kullanılıyor mu?
- [ ] Memory leak kontrolü yapıldı mı?

### Production
- [ ] Load testing yapıldı mı?
- [ ] Resource limitleri ayarlandı mı?
- [ ] Monitoring aktif mi?
- [ ] Auto-scaling kuralları belirlendi mi?
- [ ] CDN kullanılıyor mu?

### Monitoring
- [ ] Response time takibi
- [ ] Error rate analizi
- [ ] Resource usage takibi
- [ ] Cache hit ratio kontrolü
- [ ] DB connection monitoring 