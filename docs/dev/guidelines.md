# Development Guidelines

## 1. Code Style ve Standartlar

### Python Style Guide
- PEP 8 standartlarına uyulmalı
- Line length: 88 karakter (black formatter)
- Docstring format: Google style
- Type hints kullanımı zorunlu

```python
from typing import List, Optional

def process_products(
    products: List[dict],
    batch_size: Optional[int] = 100
) -> List[dict]:
    """Ürünleri toplu işler.

    Args:
        products: İşlenecek ürün listesi
        batch_size: Batch başına ürün sayısı

    Returns:
        İşlenmiş ürün listesi

    Raises:
        ValidationError: Ürün validasyonu başarısız olduğunda
    """
    pass
```

### Git Conventions

#### Branch Stratejisi
```
main           # Production
  ↑
develop        # Development/Staging
  ↑
feature/*      # Yeni özellikler
bugfix/*       # Bug fixes
hotfix/*       # Production hotfixes
```

#### Commit Mesajları
```
<type>(<scope>): <description>

[optional body]

[optional footer]

Types:
- feat: Yeni özellik
- fix: Bug fix
- docs: Dokümantasyon
- style: Kod formatı
- refactor: Refactoring
- test: Test ekleme/güncelleme
- chore: Genel bakım

Örnek:
feat(sync): add product sync retry mechanism
```

## 2. Test Stratejisi

### Test Piramidi
```
     E2E      (10%)
   Integration (30%)
     Unit      (60%)
```

### Test Tipleri ve Örnekler

#### Unit Tests
```python
# tests/unit/test_product_service.py
class TestProductService:
    def test_validate_product(self):
        product = {"sku": "123", "price": -1}
        with pytest.raises(ValidationError):
            ProductService.validate_product(product)

    @pytest.mark.asyncio
    async def test_get_product(self, mock_db):
        mock_db.get_product.return_value = {"id": 1}
        service = ProductService(db=mock_db)
        result = await service.get_product(1)
        assert result["id"] == 1
```

#### Integration Tests
```python
# tests/integration/test_sync.py
@pytest.mark.integration
class TestProductSync:
    @pytest.mark.asyncio
    async def test_sync_flow(
        self,
        woo_service,
        wolvox_service,
        redis_client
    ):
        # Test setup
        product = create_test_product()
        
        # Execute sync
        sync_service = SyncService(
            woo=woo_service,
            wolvox=wolvox_service,
            cache=redis_client
        )
        result = await sync_service.sync_product(product)
        
        # Verify results
        assert result.status == "success"
        assert await woo_service.get_product(product.id) is not None
```

#### E2E Tests
```python
# tests/e2e/test_api.py
@pytest.mark.e2e
class TestAPI:
    async def test_product_lifecycle(self, client):
        # Create product
        response = await client.post(
            "/api/v1/products",
            json={"name": "Test", "price": 100}
        )
        product_id = response.json()["id"]
        
        # Update product
        await client.put(
            f"/api/v1/products/{product_id}",
            json={"price": 200}
        )
        
        # Verify sync
        await asyncio.sleep(2)  # Wait for sync
        response = await client.get(f"/api/v1/products/{product_id}")
        assert response.json()["price"] == 200
```

## 3. Code Review Süreci

### PR Template
```markdown
## Değişiklik Açıklaması
- 

## Test Stratejisi
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No linting errors
- [ ] Type hints complete
- [ ] Metrics/logging added
```

### Review Kriterleri
1. Kod kalitesi
   - Clean code prensipleri
   - SOLID prensipleri
   - DRY prensibi
2. Test coverage
   - Yeni kod için testler
   - Edge cases
3. Performance
   - N+1 sorguları
   - Gereksiz DB çağrıları
   - Cache kullanımı
4. Security
   - Input validation
   - SQL injection koruması
   - Authentication/Authorization
5. Documentation
   - Docstrings
   - API docs
   - README updates

## 4. Monitoring ve Logging

### Metrics
```python
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['endpoint']
)
```

### Structured Logging
```python
import structlog

logger = structlog.get_logger()

async def process_order(order_id: int):
    logger.info(
        "processing_order",
        order_id=order_id,
        timestamp=datetime.now().isoformat()
    )
```

## State Yönetimi

### Global State
Uygulama state'i `app_state` dictionary'sinde merkezi olarak yönetilir:

```python
app_state = {
    'woo_service': WooCommerceService(),
    'media_service': WooCommerceMediaService()
}
```

### Lifecycle Events
- `startup_event()`: Servisleri başlatır ve state'i hazırlar
- `shutdown_event()`: Servisleri temizler ve kaynakları serbest bırakır

### Best Practices
- State erişimi için her zaman `app_state` dictionary'sini kullanın
- Servis başlatma/kapatma işlemlerini lifecycle event'lerinde yapın
- State değişikliklerini log'layın

## Metrik Toplama

### Sistem Metrikleri
```python
await update_system_metrics()  # CPU, RAM, Disk kullanımı
await update_system_info()     # Platform, Python versiyonu
await update_connection_pool() # Bağlantı havuzu durumu
```

### Servis Metrikleri
Her servis kendi metriklerini `registry` attribute'unda tutar:
```python
if hasattr(service, 'registry'):
    REGISTRY.register(service.registry)
```

## Error Handling

### Genel Kurallar
1. Her hatayı log'layın
2. HTTP isteklerinde uygun status code kullanın
3. Kullanıcıya anlamlı hata mesajları döndürün

### Örnek:
```python
try:
    result = await some_operation()
except Exception as e:
    logger.error(f"❌ Hata: {str(e)}")
    raise HTTPException(status_code=400, detail=str(e)) 