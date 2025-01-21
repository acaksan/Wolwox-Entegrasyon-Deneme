from dataclasses import dataclass
from typing import List, Optional
import fdb  # Firebird veritabanı için

@dataclass
class TireProduct:
    id: int
    brand: str
    model: str
    size: str
    season: str  # Yaz/Kış/4 Mevsim
    stock: int
    price: float
    description: Optional[str] = None

class WolvoxConnector:
    def __init__(self, config):
        self.connection = None
        self.config = config
    
    def connect(self):
        """Wolvox Firebird veritabanına bağlanır"""
        self.connection = fdb.connect(
            host=self.config.WOLVOX_HOST,
            database=self.config.WOLVOX_DB,
            user=self.config.WOLVOX_USER,
            password=self.config.WOLVOX_PASSWORD
        )
    
    def get_products(self) -> List[TireProduct]:
        """Lastik ürünlerini getirir"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT 
                STK_KODU, STOK_ADI, GRUP_KODU, 
                BAKIYE, SATIS_FIYATI1 
            FROM TBLSTSABIT 
            WHERE GRUP_KODU LIKE 'LASTIK%'
        """)
        return [TireProduct(*row) for row in cursor.fetchall()] 