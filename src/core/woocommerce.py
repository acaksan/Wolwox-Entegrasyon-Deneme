from woocommerce import API
from typing import List
from .wolvox import TireProduct

class WooCommerceSync:
    def __init__(self, config):
        self.wcapi = API(
            url=config.WC_URL,
            consumer_key=config.WC_KEY,
            consumer_secret=config.WC_SECRET,
            version="wc/v3"
        )
    
    def sync_product(self, tire: TireProduct):
        """Ürünü WooCommerce'e senkronize eder"""
        data = {
            "name": f"{tire.brand} {tire.model} {tire.size}",
            "type": "simple",
            "regular_price": str(tire.price),
            "description": tire.description,
            "stock_quantity": tire.stock,
            "manage_stock": True,
            "attributes": [
                {"name": "Marka", "visible": True, "options": [tire.brand]},
                {"name": "Ebat", "visible": True, "options": [tire.size]},
                {"name": "Sezon", "visible": True, "options": [tire.season]}
            ]
        }
        return self.wcapi.post("products", data) 