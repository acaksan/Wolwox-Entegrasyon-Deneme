# Gelişmiş Troubleshooting Rehberi

## 1. Sistem Performans Analizi

### CPU ve Memory Profiling
```bash
# CPU profiling
py-spy record -o profile.svg --pid <PID>

# Memory profiling
memray run app.py
memray flamegraph

# Garbage collection analizi
gc.set_debug(gc.DEBUG_STATS)
```

### Network Analizi
```bash
# Network trafiği
tcpdump -i any port 8000 -w capture.pcap

# Bağlantı durumu
netstat -tunapls | grep python

# Socket analizi
lsof -i :8000
```

## 2. Database Troubleshooting

### Firebird Analizi
```sql
-- Active transactions
SELECT 
    t.mon$transaction_id,
    t.mon$state,
    t.mon$timestamp,
    a.mon$user,
    a.mon$remote_address
FROM mon$transactions t
JOIN mon$attachments a ON t.mon$attachment_id = a.mon$attachment_id;

-- Lock analizi
SELECT 
    l.mon$lock_type,
    l.mon$object_name,
    a.mon$user,
    a.mon$remote_address
FROM mon$lock l
JOIN mon$attachments a ON l.mon$attachment_id = a.mon$attachment_id;
```

### Query Performance
```python
# Query execution plan
async def analyze_query(query: str):
    async with db.transaction() as tx:
        plan = await tx.fetch_one(
            f"EXPLAIN PLAN FOR {query}"
        )
        return plan

# Slow query logging
logging.getLogger('database').setLevel(logging.DEBUG)
```

## 3. Sync Troubleshooting

### Data Consistency Check
```python
async def verify_sync_status():
    # WooCommerce ürünlerini al
    woo_products = await woo_service.get_products()
    
    # Wolvox ürünlerini al
    wolvox_products = await wolvox_service.get_products()
    
    # Karşılaştır
    mismatches = []
    for wp in woo_products:
        vp = next(
            (p for p in wolvox_products if p['sku'] == wp['sku']),
            None
        )
        if not vp or wp['stock_quantity'] != vp['stock']:
            mismatches.append({
                'sku': wp['sku'],
                'woo_stock': wp['stock_quantity'],
                'volvox_stock': vp['stock'] if vp else None
            })
    
    return mismatches
```

### Event Debugging
```python
class EventDebugger:
    def __init__(self):
        self.events = []
        
    async def capture_event(self, event_type: str, data: dict):
        self.events.append({
            'type': event_type,
            'data': data,
            'timestamp': datetime.now()
        })
        
    async def analyze_events(self, time_window: int = 3600):
        # Son 1 saatteki eventleri analiz et
        recent = [
            e for e in self.events
            if (datetime.now() - e['timestamp']).seconds < time_window
        ]
        
        return {
            'total': len(recent),
            'by_type': Counter(e['type'] for e in recent),
            'error_rate': sum(1 for e in recent if 'error' in e['data']) / len(recent)
        }
```

## 4. Cache Troubleshooting

### Redis Analizi
```bash
# Memory analizi
redis-cli info memory

# Key dağılımı
redis-cli --scan --pattern '*' | awk -F: '{print $1}' | sort | uniq -c

# Büyük keyler
redis-cli --bigkeys

# Slow log
redis-cli slowlog get 10
```

### Cache Pattern Analizi
```python
async def analyze_cache_patterns():
    # Hit/miss oranları
    hits = await redis.get('cache_hits')
    misses = await redis.get('cache_misses')
    
    # Key yaşam süreleri
    keys = await redis.keys('*')
    ttls = {
        k: await redis.ttl(k)
        for k in keys
    }
    
    # Memory kullanımı
    memory_stats = await redis.info('memory')
    
    return {
        'hit_ratio': hits / (hits + misses),
        'key_count': len(keys),
        'avg_ttl': sum(ttls.values()) / len(ttls),
        'memory_used': memory_stats['used_memory_human']
    }
```

## 5. Log Analizi Araçları

### Log Aggregation
```python
class LogAnalyzer:
    def __init__(self, log_path: str):
        self.log_path = log_path
        
    async def analyze_errors(self, time_window: int = 3600):
        errors = []
        now = datetime.now()
        
        async with aiofiles.open(self.log_path) as f:
            async for line in f:
                log = json.loads(line)
                if (
                    log['level'] == 'ERROR' and
                    (now - datetime.fromisoformat(log['timestamp'])).seconds < time_window
                ):
                    errors.append(log)
        
        return {
            'total': len(errors),
            'by_module': Counter(e['module'] for e in errors),
            'by_type': Counter(e.get('error_type') for e in errors),
            'most_common': Counter(e['message'] for e in errors).most_common(5)
        }
```

### Metrics Analizi
```python
async def analyze_metrics(start_time: datetime, end_time: datetime):
    # Prometheus'tan metrikleri çek
    query = f"""
    sum(rate(http_requests_total[5m])) by (endpoint)
    and timestamp >= {start_time.timestamp()}
    and timestamp <= {end_time.timestamp()}
    """
    
    result = await prometheus.query_range(
        query,
        start=start_time,
        end=end_time,
        step='5m'
    )
    
    return {
        'total_requests': sum(r['values'][-1][1] for r in result),
        'by_endpoint': {
            r['metric']['endpoint']: r['values'][-1][1]
            for r in result
        },
        'error_rate': await get_error_rate(start_time, end_time)
    }
```

## 6. Recovery Procedures

### Data Recovery
```python
async def recover_sync_state():
    try:
        # 1. Sync'i durdur
        await sync_service.stop()
        
        # 2. Son başarılı sync noktasını bul
        last_sync = await get_last_successful_sync()
        
        # 3. O noktadan itibaren tekrar sync et
        await sync_service.sync_from_checkpoint(last_sync)
        
        # 4. Tutarlılığı kontrol et
        mismatches = await verify_sync_status()
        if mismatches:
            raise SyncError(f"Found {len(mismatches)} mismatches")
            
    finally:
        # 5. Sync'i tekrar başlat
        await sync_service.start()
```

### Service Recovery
```python
async def recover_service(service_name: str):
    # 1. Servisi durdur
    await stop_service(service_name)
    
    # 2. State'i temizle
    await clean_service_state(service_name)
    
    # 3. Bağımlılıkları kontrol et
    deps_healthy = await check_dependencies(service_name)
    if not deps_healthy:
        raise RecoveryError("Dependencies not healthy")
    
    # 4. Servisi başlat
    await start_service(service_name)
    
    # 5. Health check
    healthy = await check_service_health(service_name)
    if not healthy:
        raise RecoveryError("Service not healthy after recovery")
```

# İleri Seviye Sorun Giderme

## Performans Analizi

### 1. CPU Profiling
```python
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Test edilecek kod
    result = service.process_items()
    
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()
```

### 2. Memory Profiling
```python
from memory_profiler import profile

@profile
async def memory_intensive_task():
    data = []
    for i in range(1000000):
        data.append(i)
    return len(data)
```

### 3. Network Analizi
```python
import aiohttp
import time

async def analyze_request():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            duration = time.time() - start
            print(f"Request took {duration:.2f}s")
            print(f"Status: {response.status}")
```

## Database Optimizasyonu

### 1. Query Analizi
```sql
EXPLAIN ANALYZE SELECT * FROM products WHERE updated_at > NOW() - INTERVAL '1 day';
```

### 2. Index Optimizasyonu
```sql
CREATE INDEX idx_products_updated_at ON products(updated_at);
```

## Concurrency Sorunları

### 1. Race Condition Tespiti
```python
import asyncio
from asyncio import Lock

class SafeCounter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0
        
    async def increment(self):
        async with self.lock:
            self.count += 1
```

### 2. Deadlock Analizi
```python
import traceback

async def detect_deadlock():
    tasks = asyncio.all_tasks()
    for task in tasks:
        if task.done():
            continue
        print(f"Task: {task.get_name()}")
        print(f"Stack:\n{''.join(traceback.format_stack())}")
```

## Security Auditing

### 1. SSL/TLS Analizi
```bash
openssl s_client -connect example.com:443 -tls1_2
```

### 2. API Security Check
```python
async def security_check():
    headers = {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            for header, value in headers.items():
                assert response.headers.get(header) == value
```

## Recovery Procedures

### 1. Data Recovery
```python
async def recover_failed_uploads():
    failed = await service.get_failed_uploads()
    for item in failed:
        try:
            await service.retry_upload(item['id'])
        except Exception as e:
            logger.error(f"Recovery failed: {str(e)}")
```

### 2. Service Recovery
```python
async def service_recovery():
    # 1. Stop all processing
    await service.pause()
    
    # 2. Clear problematic data
    await cache.flushall()
    
    # 3. Reinitialize services
    await service.reinitialize()
    
    # 4. Resume processing
    await service.resume()
```

## Monitoring ve Alerting

### 1. Custom Metrics
```python
from prometheus_client import Counter, Gauge

error_counter = Counter(
    'app_errors_total',
    'Total number of application errors',
    ['type']
)

processing_time = Gauge(
    'app_processing_time_seconds',
    'Time spent processing requests'
)
```

### 2. Alert Rules
```yaml
groups:
- name: app_alerts
  rules:
  - alert: HighErrorRate
    expr: rate(app_errors_total[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: High error rate detected
``` 