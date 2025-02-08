"""Metrik toplama ve raporlama"""

import time
from typing import Any, Dict

from prometheus_client import (CollectorRegistry, Counter, Gauge, Histogram,
                               Summary, generate_latest)

# Metrik kayıt defteri
registry = CollectorRegistry()

# Temel metrikler
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status'],
    registry=registry
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    registry=registry
)

active_connections = Gauge(
    'active_connections',
    'Number of active connections',
    registry=registry
)

def reset_metrics():
    """Test için metrikleri sıfırla"""
    registry.clear()

__all__ = [
    'registry',
    'reset_metrics',
    'http_requests_total',
    'http_request_duration_seconds',
    'active_connections'
] 