import time
from functools import wraps

from prometheus_client import Counter, Histogram

# Metrikler
SYNC_REQUESTS = Counter(
    'wolvox_sync_requests_total',
    'Toplam senkronizasyon istekleri',
    ['type']
)

SYNC_DURATION = Histogram(
    'wolvox_sync_duration_seconds',
    'Senkronizasyon süresi',
    ['type']
)

def track_sync_duration(func):
    """Senkronizasyon süresini ölçen decorator"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        sync_type = func.__name__.replace('sync_', '')
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            SYNC_REQUESTS.labels(type=sync_type).inc()
            return result
        finally:
            duration = time.time() - start_time
            SYNC_DURATION.labels(type=sync_type).observe(duration)
    
    return wrapper 