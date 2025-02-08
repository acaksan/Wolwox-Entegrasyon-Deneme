from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.core.config import settings

# Veritabanı engine'ini oluştur
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# SessionLocal factory'sini oluştur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class'ı oluştur
Base = declarative_base()

# Database bağlantısı için dependency
def get_db() -> Generator:
    """
    Veritabanı oturumu için dependency injection.
    Her request için yeni bir oturum oluşturur ve işlem bitince kapatır.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close() 