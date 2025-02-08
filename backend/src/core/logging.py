"""Loglama yapılandırması."""

import json
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Optional

from core.settings import get_settings

settings = get_settings()

def setup_logger(name: str) -> logging.Logger:
    """Logger yapılandırması."""
    
    # Log dizinini oluştur
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Logger'ı yapılandır
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    
    # Formatı ayarla
    if settings.LOG_FORMAT == "json":
        formatter = logging.Formatter(
            '{"timestamp":"%(asctime)s", "name":"%(name)s", "level":"%(levelname)s", "message":"%(message)s"}'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # Dosya handler'ı
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(settings.LOG_LEVEL)
    file_handler.setFormatter(formatter)
    
    # Konsol handler'ı
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL)
    console_handler.setFormatter(formatter)
    
    # Handler'ları ekle
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_event(level: str, module: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
    """Olay logla."""
    logger = logging.getLogger(module)
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "module": module,
        "message": message,
        "details": details or {}
    }
    
    log_message = json.dumps(log_data)
    getattr(logger, level.lower())(log_message)

def log_error(module: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
    """Hata logla."""
    log_event("ERROR", module, message, details)

def log_info(module: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
    """Bilgi logla."""
    log_event("INFO", module, message, details)

def log_warning(module: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
    """Uyarı logla."""
    log_event("WARNING", module, message, details)

def notify_admin(message: str, context: Optional[Dict[str, Any]] = None) -> None:
    """Yöneticiye bildirim gönder."""
    logger = logging.getLogger("admin_notifications")
    
    notification = {
        "timestamp": datetime.now().isoformat(),
        "message": message,
        "context": context or {}
    }
    
    logger.error(json.dumps(notification))

# Ana logger'ı oluştur
logger = setup_logger("wolvox_integration")

__all__ = ["logger", "log_error", "log_info", "log_warning", "notify_admin"] 