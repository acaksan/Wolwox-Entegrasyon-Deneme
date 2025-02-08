# Test Rehberi

## Test Yapısı

### 1. Unit Tests
`tests/unit/` dizininde bulunur ve tekil bileşenleri test eder.

```python
# tests/unit/test_product_service.py
import pytest
from src.services import WooCommerceProductService

class TestProductService:
    @pytest.mark.asyncio
    async def test_create_product(self, mocker):
        # Mock WooCommerce API
        mock_api = mocker.patch('src.services.woocommerce_service.API')
        mock_api.return_value.post.return_value.json.return_value = {
            'id': 1,
            'name': 'Test Product'
        }
        
        service = WooCommerceProductService()
        result = await service.create_product({
            'name': 'Test Product',
            'sku': 'TST001'
        })
        
        assert result['id'] == 1
        assert result['name'] == 'Test Product'
```

### 2. Integration Tests
`tests/integration/` dizininde bulunur ve servisler arası entegrasyonu test eder.

```python
# tests/integration/test_sync_service.py
@pytest.mark.integration
class TestSyncService:
    @pytest.mark.asyncio
    async def test_product_sync(self, woo_service, wolvox_service):
        sync_service = SyncService(woo_service, wolvox_service)
        
        # Test ürünü oluştur
        product = await woo_service.create_product({
            'name': 'Test Product',
            'sku': 'TST001'
        })
        
        # Senkronizasyon
        result = await sync_service.sync_product(product['id'])
        assert result['status'] == 'success'
        
        # Wolvox'ta kontrol et
        wolvox_product = await wolvox_service.get_product(product['sku'])
        assert wolvox_product is not None
```

### 3. E2E Tests
`tests/e2e/` dizininde bulunur ve uçtan uca senaryoları test eder.

```python
# tests/e2e/test_order_flow.py
@pytest.mark.e2e
class TestOrderFlow:
    @pytest.mark.asyncio
    async def test_complete_order_flow(self, api_client):
        # 1. Ürün oluştur
        product = await api_client.post('/products', json={
            'name': 'Test Product',
            'sku': 'TST001',
            'price': '99.90'
        })
        
        # 2. Sipariş oluştur
        order = await api_client.post('/orders', json={
            'line_items': [{
                'product_id': product['id'],
                'quantity': 1
            }]
        })
        
        # 3. Siparişi onayla
        result = await api_client.put(
            f'/orders/{order["id"]}',
            json={'status': 'completed'}
        )
        
        assert result['status'] == 'completed'
        
        # 4. Stok kontrolü
        updated_product = await api_client.get(f'/products/{product["id"]}')
        assert updated_product['stock_quantity'] == product['stock_quantity'] - 1
```

## Test Fixtures

### Temel Fixtures
```python
# tests/conftest.py
import pytest
from src.core.config import get_settings

@pytest.fixture
def settings():
    return get_settings()

@pytest.fixture
async def woo_service():
    return WooCommerceService()

@pytest.fixture
async def test_product(woo_service):
    product = await woo_service.create_product({...})
    yield product
    await woo_service.delete_product(product['id'])
```

### Mock Fixtures
```python
@pytest.fixture
def mock_woo_api(mocker):
    return mocker.patch('src.services.woocommerce_service.API')

@pytest.fixture
def mock_redis(mocker):
    return mocker.patch('src.core.cache.redis.Redis')
```

## Test Kategorileri

### 1. Validation Tests
```python
@pytest.mark.parametrize('invalid_data,expected_error', [
    ({'name': ''}, 'Name is required'),
    ({'price': -1}, 'Price must be positive'),
    ({'sku': 'AB'}, 'SKU must be at least 3 characters')
])
async def test_product_validation(invalid_data, expected_error):
    with pytest.raises(ValidationError) as exc:
        await service.create_product(invalid_data)
    assert str(exc.value) == expected_error
```

### 2. Error Handling Tests
```python
async def test_api_error_handling():
    with pytest.raises(WooCommerceError) as exc:
        await service.get_product(999999)
    assert exc.value.status_code == 404
```

### 3. Performance Tests
```python
@pytest.mark.benchmark
async def test_bulk_operation_performance(benchmark):
    result = await benchmark(
        service.bulk_update_products,
        [{'id': i, 'stock': 100} for i in range(100)]
    )
    assert len(result) == 100
```

## Test Coverage

### Coverage Hedefleri
- Unit Tests: %90+
- Integration Tests: %80+
- Overall Coverage: %85+

### Coverage Raporu
```bash
# Coverage raporu oluştur
make coverage

# HTML raporu görüntüle
open htmlcov/index.html
```

## Test Best Practices

1. **Test İzolasyonu**
   - Her test kendi verisini oluşturmalı
   - Test sonrası temizlik yapılmalı
   - Testler birbirinden bağımsız olmalı

2. **Naming Conventions**
   - test_should_do_something_when_condition
   - test_method_name_scenario_expected_behavior

3. **Assertion Best Practices**
   - Her testte tek bir konsepti test et
   - Anlamlı assertion mesajları kullan
   - Edge case'leri unutma

4. **Mock Kullanımı**
   - Sadece gerekli yerlerde mock kullan
   - Mock'ları test scope'unda tut
   - Side effect'leri test et 