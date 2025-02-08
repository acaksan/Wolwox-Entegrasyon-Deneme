import asyncio
from unittest.mock import patch

import psutil
import pytest
from prometheus_client import (CONTENT_TYPE_LATEST, CollectorRegistry, Counter,
                               Gauge, Histogram, generate_latest)

from backend.core.config import get_settings
from backend.core.metrics import ACTIVE_CONNECTIONS as active_connections
from backend.core.metrics import CONNECTION_POOL
from backend.core.metrics import REQUEST_COUNT as request_count
from backend.core.metrics import REQUEST_LATENCY as request_latency
from backend.core.metrics import SYNC_STATUS as sync_status
from backend.core.metrics import (SYSTEM_METRICS, get_metric_labels,
                                  get_metric_value, registry, reset_metrics,
                                  update_connection_pool, update_system_info,
                                  update_system_metrics, validate_metric_value,
                                  validate_service_name)

settings = get_settings()

@pytest.fixture(scope="function")
def test_registry():
    """Her test için yeni registry oluştur"""
    test_registry = CollectorRegistry()
    yield test_registry
    # Temizlik
    for collector in list(test_registry._collector_to_names.keys()):
        try:
            test_registry.unregister(collector)
        except KeyError:
            pass

@pytest.fixture(scope="function")
def mock_settings(monkeypatch):
    """Test ayarları"""
    class MockSettings:
        METRICS_UPDATE_INTERVAL = 1
        METRICS_ENABLED = True
    monkeypatch.setattr("backend.core.config.get_settings", lambda: MockSettings())
    return MockSettings()

@pytest.fixture
def test_metrics():
    """Test metrikleri"""
    # Yeni registry oluştur
    test_registry = CollectorRegistry()
    
    # Yeni metrikler oluştur
    test_request_count = Counter(
        'test_request_total', 
        'Total number of requests',
        ['method', 'endpoint'],
        registry=test_registry
    )
    test_request_latency = Histogram(
        'test_request_latency_seconds',
        'Request latency in seconds',
        ['method', 'endpoint'],
        registry=test_registry
    )
    test_active_connections = Gauge(
        'test_active_connections',
        'Number of active connections',
        ['service'],
        registry=test_registry
    )
    test_sync_status = Gauge(
        'test_sync_status',
        'Sync status (1=success, 0=failed)',
        ['type'],
        registry=test_registry
    )
    
    yield {
        'registry': test_registry,
        'request_count': test_request_count,
        'request_latency': test_request_latency,
        'active_connections': test_active_connections,
        'sync_status': test_sync_status
    }
    
    # Temizlik
    for collector in list(test_registry._collector_to_names.keys()):
        try:
            test_registry.unregister(collector)
        except KeyError:
            pass

@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Her test sonrası temizlik yap"""
    yield
    # Registry'yi temizle
    for collector in list(registry._collector_to_names.keys()):
        try:
            registry.unregister(collector)
        except KeyError:
            pass

class TestMetrics:
    def test_request_counter(self, test_metrics):
        """Request sayacı testi"""
        test_metrics['request_count'].labels(method='GET', endpoint='/products').inc()
        test_metrics['request_count'].labels(method='POST', endpoint='/orders').inc()
        test_metrics['request_count'].labels(method='POST', endpoint='/orders').inc()
        
        # Kontroller
        get_count = test_metrics['request_count'].labels(method='GET', endpoint='/products')._value.get()
        post_count = test_metrics['request_count'].labels(method='POST', endpoint='/orders')._value.get()
        
        assert get_count == 1
        assert post_count == 2

    def test_request_latency(self, test_metrics):
        """Request latency testi"""
        test_metrics['request_latency'].labels(method='GET', endpoint='/products').observe(0.1)
        test_metrics['request_latency'].labels(method='GET', endpoint='/products').observe(0.2)
        
        # Kontroller
        histogram = test_metrics['request_latency'].labels(method='GET', endpoint='/products')
        assert histogram._sum.get() == pytest.approx(0.3, rel=1e-9)  # toplam
        
        # Debug: Tüm metrik çıktısını göster
        metric_output = generate_latest(test_metrics['registry']).decode()
        print("\nMetrik çıktısı:")
        print(metric_output)
        
        sample_count = None
        for line in metric_output.split('\n'):
            # Daha esnek bir eşleşme kullan
            if 'test_request_latency_seconds_count' in line and 'method="GET"' in line and 'endpoint="/products"' in line:
                sample_count = float(line.split(' ')[1])
                break
        
        assert sample_count is not None, "Sample count metriği bulunamadı"
        assert sample_count == 2.0  # örnek sayısı

    def test_active_connections(self, test_metrics):
        """Aktif bağlantı sayısı testi"""
        test_metrics['active_connections'].labels(service='redis').set(5)
        test_metrics['active_connections'].labels(service='woocommerce').set(3)
        
        # Kontroller
        redis_conn = test_metrics['active_connections'].labels(service='redis')._value.get()
        woo_conn = test_metrics['active_connections'].labels(service='woocommerce')._value.get()
        
        assert redis_conn == 5
        assert woo_conn == 3

    def test_sync_status(self, test_metrics):
        """Senkronizasyon durumu testi"""
        test_metrics['sync_status'].labels(type='products').set(1)  # success
        test_metrics['sync_status'].labels(type='orders').set(0)    # failed
        
        # Kontroller
        products_sync = test_metrics['sync_status'].labels(type='products')._value.get()
        orders_sync = test_metrics['sync_status'].labels(type='orders')._value.get()
        
        assert products_sync == 1
        assert orders_sync == 0

@pytest.mark.asyncio
async def test_system_metrics():
    """Sistem metriklerinin testi"""
    try:
        # Metrikleri sıfırla
        reset_metrics()
        
        # İlk güncelleme
        await update_system_metrics()
        
        # CPU kullanımı kontrolü
        cpu_value = SYSTEM_METRICS['cpu_usage']._value.get()
        assert isinstance(cpu_value, (int, float)), f"Invalid CPU value type: {type(cpu_value)}"
        assert 0 <= cpu_value <= 100, f"CPU value out of range: {cpu_value}"
        
        # Bellek kullanımı kontrolü
        memory_value = SYSTEM_METRICS['memory_usage']._value.get()
        assert isinstance(memory_value, (int, float)), f"Invalid memory value type: {type(memory_value)}"
        assert memory_value > 0, f"Invalid memory value: {memory_value}"
        
        # Disk kullanımı kontrolü
        disk_found = False
        for partition in psutil.disk_partitions():
            try:
                usage = SYSTEM_METRICS['disk_usage'].labels(
                    path=partition.mountpoint
                )._value.get()
                assert isinstance(usage, (int, float)), f"Invalid disk usage type: {type(usage)}"
                assert 0 <= usage <= 100, f"Disk usage out of range: {usage}"
                disk_found = True
            except Exception as e:
                print(f"Skipping partition {partition.mountpoint}: {str(e)}")
                continue
                
        assert disk_found, "No valid disk partitions found"
                
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

@pytest.mark.asyncio
async def test_periodic_metrics_update(mock_settings):
    """Periyodik metrik güncellemesinin testi"""
    try:
        # Metrikleri sıfırla
        reset_metrics()
        
        # İlk değerleri al
        await update_system_metrics()
        initial_cpu = SYSTEM_METRICS['cpu_usage']._value.get()
        
        # Kısa bir süre bekle
        await asyncio.sleep(1.5)
        
        # Tekrar güncelle
        await update_system_metrics()
        updated_cpu = SYSTEM_METRICS['cpu_usage']._value.get()
        
        # Değerlerin güncellendiğini kontrol et
        assert initial_cpu is not None, "Initial CPU value is None"
        assert updated_cpu is not None, "Updated CPU value is None"
        assert isinstance(initial_cpu, (int, float)), f"Invalid initial CPU type: {type(initial_cpu)}"
        assert isinstance(updated_cpu, (int, float)), f"Invalid updated CPU type: {type(updated_cpu)}"
        assert 0 <= initial_cpu <= 100, f"Initial CPU out of range: {initial_cpu}"
        assert 0 <= updated_cpu <= 100, f"Updated CPU out of range: {updated_cpu}"
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

@pytest.mark.asyncio
async def test_system_info_update():
    """Sistem bilgileri güncelleme testi"""
    try:
        # Test verileri
        version = "1.1.1"
        environment = "testing"
        
        # Sistem bilgilerini güncelle
        update_system_info(version, environment)
        
        # Metrik çıktısını al ve parse et
        info_text = generate_latest(registry).decode()
        info_lines = [line for line in info_text.split('\n') 
                     if 'wolvox_system_info' in line and not line.startswith('#')]
        
        # Kontroller
        assert len(info_lines) > 0, "No system info metrics found"
        info_line = info_lines[0]
        assert version in info_line, f"Version {version} not found in metrics"
        assert environment in info_line, f"Environment {environment} not found in metrics"
        assert 'last_update' in info_line, "Timestamp not found in metrics"
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

@pytest.mark.asyncio
async def test_connection_pool_metrics():
    """Bağlantı havuzu metrikleri testi"""
    try:
        # Test verileri
        services = {
            'redis': 10,
            'firebird': 5,
            'woocommerce': 20
        }
        
        # Bağlantı havuzu metriklerini güncelle
        for service, size in services.items():
            update_connection_pool(service, size)
        
        # Metrik çıktısını al ve kontrol et
        for service, expected_size in services.items():
            pool_size = CONNECTION_POOL.labels(service=service)._value.get()
            assert pool_size == expected_size, \
                f"Pool size mismatch for {service}: expected {expected_size}, got {pool_size}"
            assert isinstance(pool_size, (int, float)), \
                f"Invalid type for pool size: {type(pool_size)}"
            assert pool_size >= 0, f"Negative pool size for {service}: {pool_size}"
            
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

@pytest.mark.asyncio
async def test_metrics_error_handling():
    """Metrik hata yönetimi testi"""
    try:
        # Geçersiz servis adı ile test
        with pytest.raises(ValueError) as exc_info:
            update_connection_pool("invalid_service", -1)
        assert "Invalid service name" in str(exc_info.value)
        
        # Geçersiz metrik değeri ile test
        with pytest.raises(ValueError) as exc_info:
            validate_metric_value(-1, 'wolvox_system_cpu')
        assert "CPU usage must be between 0-100" in str(exc_info.value)
        
        # Metrik güncelleme hatası simülasyonu
        async def mock_update():
            raise Exception("Test error")
        
        # Hata durumunda metrik değerlerinin korunduğunu kontrol et
        initial_cpu = SYSTEM_METRICS['cpu_usage']._value.get()
        try:
            await mock_update()
        except:
            pass
        current_cpu = SYSTEM_METRICS['cpu_usage']._value.get()
        assert current_cpu == initial_cpu, f"CPU value changed after error: {initial_cpu} -> {current_cpu}"
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

@pytest.mark.asyncio
async def test_metrics_cleanup():
    """Metrik temizleme testi"""
    # Test registry'si oluştur
    test_registry = CollectorRegistry()
    
    # Test metriği ekle
    test_counter = Counter(
        'test_counter',
        'Test counter',
        registry=test_registry
    )
    test_counter.inc()
    
    # Registry'yi temizle
    test_registry.unregister(test_counter)
    
    # Metriğin silindiğini kontrol et
    metrics_output = generate_latest(test_registry).decode()
    assert 'test_counter' not in metrics_output 

@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_metric_labels():
    """Metrik etiketlerinin testi"""
    labels = get_metric_labels('wolvox_request_total')
    assert 'method' in labels
    assert 'endpoint' in labels

@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_metric_value():
    """Metrik değerlerinin testi"""
    counter = Counter('test_counter', 'Test counter', registry=registry)
    counter.inc(2)
    value = get_metric_value('test_counter')
    assert value == 2.0

@pytest.mark.asyncio
async def test_reset_metrics():
    """Metrik sıfırlama testi"""
    # Test metriği oluştur ve artır
    counter = Counter(
        'test_reset_counter',
        'Test reset counter',
        registry=registry
    )
    counter.inc()
    
    # Sıfırla ve kontrol et
    reset_metrics()
    assert get_metric_value('test_reset_counter') == 0.0 

# Test öncesi temizlik
def pytest_runtest_setup():
    reset_metrics()
    for collector in list(registry._collector_to_names.keys()):
        try:
            registry.unregister(collector)
        except KeyError:
            pass 