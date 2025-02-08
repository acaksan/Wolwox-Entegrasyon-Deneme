from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr
from src.database.base import Base


class BaseModel(Base):
    """
    Tüm modeller için temel sınıf.
    Her modelde olması gereken ortak alanları içerir.
    """
    
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Tablo ismi için snake_case convention
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def dict(self) -> dict[str, Any]:
        """
        Model verilerini dictionary olarak döndürür
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BaseModelConfig(BaseModel):
    """Temel model konfigürasyonu"""
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    ) 