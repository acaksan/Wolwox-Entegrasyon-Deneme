from typing import Optional

from pydantic import BaseModel


class StockBase(BaseModel):
    product_id: str
    quantity: int
    
class StockCheck(StockBase):
    product_name: str
    sku: Optional[str] = None
    status: str  # "normal", "low", "out_of_stock"
    threshold: Optional[int] = None
    
    class Config:
        orm_mode = True
        
class StockUpdate(BaseModel):
    quantity: int
    
    class Config:
        orm_mode = True 