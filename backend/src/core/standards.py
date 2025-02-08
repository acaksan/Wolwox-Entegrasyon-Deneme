from enum import Enum


class ModelPrefix(str, Enum):
    """Model prefix standartları"""
    WOLVOX = "Wlx"  # Wolvox modelleri
    WOOCOMMERCE = "Woo"  # WooCommerce modelleri
    SYNC = "Sync"  # Senkronizasyon modelleri

class TablePrefix(str, Enum):
    """Tablo prefix standartları"""
    WOLVOX = "STK"  # Stok tabloları
    SYNC = "SYNC"  # Senkronizasyon tabloları
    LOG = "LOG"  # Log tabloları

class FileStructure:
    """Dosya yapısı standartları"""
    MODELS = "src/models"
    REPOSITORIES = "src/repositories"
    SERVICES = "src/services"
    API = "src/api"
    CORE = "src/core"
    TESTS = "tests" 