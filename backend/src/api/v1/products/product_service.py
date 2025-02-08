from typing import List, Optional

from sqlalchemy.orm import Session
from src.api.schemas.product import ProductCreate, ProductInDB, ProductUpdate
from src.repositories.product_repository import ProductRepository
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ProductService:
    """
    Ürün işlemleri için servis sınıfı.
    Repository pattern kullanarak veritabanı işlemlerini yönetir.
    """
    
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
    
    def create_product(self, product: ProductCreate) -> ProductInDB:
        """
        Yeni ürün oluşturur
        """
        try:
            logger.info(f"Yeni ürün oluşturuluyor: {product.wolvox_id}")
            db_product = self.repository.create(product)
            return ProductInDB.model_validate(db_product)
        except Exception as e:
            logger.error(f"Ürün oluşturma hatası: {str(e)}")
            raise
    
    def get_product(self, product_id: int) -> Optional[ProductInDB]:
        """
        ID'ye göre ürün getirir
        """
        try:
            db_product = self.repository.get_by_id(product_id)
            if db_product:
                return ProductInDB.model_validate(db_product)
            logger.warning(f"Ürün bulunamadı: {product_id}")
            return None
        except Exception as e:
            logger.error(f"Ürün getirme hatası: {str(e)}")
            raise
    
    def get_product_by_wolvox_id(self, wolvox_id: str) -> Optional[ProductInDB]:
        """
        Wolvox ID'ye göre ürün getirir
        """
        try:
            db_product = self.repository.get_by_wolvox_id(wolvox_id)
            if db_product:
                return ProductInDB.model_validate(db_product)
            logger.warning(f"Wolvox ID ile ürün bulunamadı: {wolvox_id}")
            return None
        except Exception as e:
            logger.error(f"Wolvox ID ile ürün getirme hatası: {str(e)}")
            raise
    
    def get_products(self, skip: int = 0, limit: int = 100) -> List[ProductInDB]:
        """
        Tüm ürünleri getirir
        """
        try:
            db_products = self.repository.get_all(skip=skip, limit=limit)
            return [ProductInDB.model_validate(p) for p in db_products]
        except Exception as e:
            logger.error(f"Ürünleri getirme hatası: {str(e)}")
            raise
    
    def update_product(self, product_id: int, product: ProductUpdate) -> Optional[ProductInDB]:
        """
        Ürün günceller
        """
        try:
            logger.info(f"Ürün güncelleniyor: {product_id}")
            db_product = self.repository.update(product_id, product)
            if db_product:
                return ProductInDB.model_validate(db_product)
            logger.warning(f"Güncellenecek ürün bulunamadı: {product_id}")
            return None
        except Exception as e:
            logger.error(f"Ürün güncelleme hatası: {str(e)}")
            raise
    
    def delete_product(self, product_id: int) -> bool:
        """
        Ürün siler
        """
        try:
            logger.info(f"Ürün siliniyor: {product_id}")
            return self.repository.delete(product_id)
        except Exception as e:
            logger.error(f"Ürün silme hatası: {str(e)}")
            raise 