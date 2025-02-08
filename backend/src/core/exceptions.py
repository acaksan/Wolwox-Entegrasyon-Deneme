"""Özel hata sınıfları."""

from typing import Any, Dict, Optional


class WolvoxException(Exception):
    """Temel Wolvox hata sınıfı."""
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class DatabaseException(WolvoxException):
    """Veritabanı hatalarını temsil eden sınıf."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="DB_ERROR",
            status_code=500,
            details=details
        )

class WooCommerceException(WolvoxException):
    """WooCommerce API hataları"""
    pass

class ConfigurationException(WolvoxException):
    """Konfigürasyon hataları için özel sınıf"""
    pass

class ValidationException(WolvoxException):
    """Doğrulama hatalarını temsil eden sınıf."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            details=details
        )

class ConnectionException(WolvoxException):
    """Bağlantı hataları"""
    pass

class ServiceError(WolvoxException):
    """Servis hatası"""
    pass

class CacheException(ServiceError):
    """Cache hatası"""
    pass

class ImageProcessingError(ServiceError):
    """Görsel işleme hatası"""
    pass

class ServiceException(WolvoxException):
    """Servis katmanı hataları"""
    pass

class SyncException(WolvoxException):
    """Senkronizasyon hataları"""
    pass

class APIException(WolvoxException):
    """API hatalarını temsil eden sınıf."""
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="API_ERROR",
            status_code=status_code,
            details=details
        )

class AuthenticationException(WolvoxException):
    """Kimlik doğrulama hataları için özel sınıf"""
    pass

class AuthorizationException(WolvoxException):
    """Yetkilendirme hataları için özel sınıf"""
    pass

class IntegrationException(WolvoxException):
    """Entegrasyon hataları için özel sınıf"""
    pass

class ResourceNotFoundException(WolvoxException):
    """Kaynak bulunamadı hataları"""
    pass

__all__ = [
    'WolvoxException',
    'ServiceError',
    'WooCommerceException',
    'DatabaseException',
    'CacheException',
    'ImageProcessingError',
    'ValidationError'
] 