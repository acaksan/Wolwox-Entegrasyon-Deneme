"""Ana uygulama modülü"""

import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from api.v1.router import api_router
from core.logging import logger
from core.settings import get_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.error_handler import setup_error_handlers

# Uygulama ayarlarını al
settings = get_settings()

# FastAPI uygulamasını oluştur
app = FastAPI(
    title=settings.APP_NAME,
    description="Wolvox ERP ve WooCommerce entegrasyon API'si",
    version="1.0.0"
)

# CORS ayarlarını yapılandır
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için tüm originlere izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Kök endpoint"""
    return {"message": "API çalışıyor!"}

# Hata yakalayıcıları ekle
setup_error_handlers(app)

# API rotalarını ekle
app.include_router(api_router, prefix="/api/v1")
