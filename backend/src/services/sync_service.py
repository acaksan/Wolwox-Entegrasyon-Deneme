"""Senkronizasyon servisi"""

from typing import Any, Dict, List, Optional, Tuple

from src.utils.logger import logger
from src.wolvox.wolvox_service import wolvox_service
from src.wolvox.woocommerce_service import WooCommerceService


class SyncService:
    """Wolvox ve WooCommerce senkronizasyon servisi"""
    
    def __init__(self):
        """Senkronizasyon servisini başlat"""
        self.wolvox = wolvox_service
        self.woo = WooCommerceService()
        
    async def _prepare_customer_data(self, woo_customer: Dict[str, Any]) -> Dict[str, Any]:
        """WooCommerce müşteri verisini Wolvox formatına dönüştür"""
        billing = woo_customer.get('billing', {})
        meta_data = {item['key']: item['value'] for item in woo_customer.get('meta_data', [])}
        
        return {
            "unvan": f"{billing.get('first_name', '')} {billing.get('last_name', '')}".strip(),
            "vergi_no": meta_data.get('vat_number', ''),
            "vergi_daire": meta_data.get('tax_office', ''),
            "adres": billing.get('address_1', ''),
            "adres2": billing.get('address_2', ''),
            "il": billing.get('state', ''),
            "ilce": billing.get('city', ''),
            "ulke": billing.get('country', 'TR'),
            "telefon": billing.get('phone', ''),
            "email": woo_customer.get('email', ''),
            "musteri_tipi": "B2C",  # Varsayılan olarak B2C
            "para_birimi": "TRY",   # Varsayılan olarak TRY
            "woo_customer_id": str(woo_customer['id'])
        }
    
    async def sync_customer(self, woo_customer_id: int) -> Optional[str]:
        """WooCommerce müşterisini Wolvox'a aktar"""
        try:
            # WooCommerce'den müşteri bilgilerini al
            woo_customer = await self.woo.get_customer(woo_customer_id)
            if not woo_customer:
                logger.error(f"WooCommerce müşterisi bulunamadı: {woo_customer_id}")
                raise ValueError(f"WooCommerce müşterisi bulunamadı: {woo_customer_id}")
            
            # Müşteri verilerini hazırla
            customer_data = await self._prepare_customer_data(woo_customer)
            
            # Önce mevcut müşteriyi bulmaya çalış
            search_params = {
                "vergi_no": customer_data["vergi_no"],
                "email": customer_data["email"],
                "telefon": customer_data["telefon"]
            }
            
            existing_customer = await self.wolvox.find_customer(search_params)
            
            if existing_customer:
                # Müşteri bulundu, bilgilerini güncelle
                success = await self.wolvox.update_customer(
                    existing_customer["musteri_kodu"],
                    customer_data
                )
                if success:
                    logger.info(f"Müşteri güncellendi: {existing_customer['musteri_kodu']}")
                    return existing_customer["musteri_kodu"]
                else:
                    logger.error(f"Müşteri güncellenemedi: {existing_customer['musteri_kodu']}")
                    raise RuntimeError(f"Müşteri güncellenemedi: {existing_customer['musteri_kodu']}")
            else:
                # Yeni müşteri oluştur
                musteri_kodu = await self.wolvox.create_customer(customer_data)
                if musteri_kodu:
                    logger.info(f"Yeni müşteri oluşturuldu: {musteri_kodu}")
                    return musteri_kodu
                else:
                    logger.error("Yeni müşteri oluşturulamadı")
                    raise RuntimeError("Yeni müşteri oluşturulamadı")

        except ValueError as e:
            logger.error(f"Müşteri senkronizasyon doğrulama hatası: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Müşteri senkronizasyon hatası: {str(e)}")
            raise RuntimeError(f"Müşteri senkronizasyon hatası: {str(e)}")

    async def get_or_create_customer(self, woo_customer_id: int) -> Optional[str]:
        """WooCommerce müşterisini Wolvox'ta bul veya oluştur"""
        try:
            # WooCommerce'den müşteri bilgilerini al
            woo_customer = await self.woo.get_customer(woo_customer_id)
            if not woo_customer:
                logger.error(f"WooCommerce müşterisi bulunamadı: {woo_customer_id}")
                raise ValueError(f"WooCommerce müşterisi bulunamadı: {woo_customer_id}")

            # Müşteri verilerini hazırla
            customer_data = await self._prepare_customer_data(woo_customer)
            
            # Önce mevcut müşteriyi bulmaya çalış
            search_params = {
                "vergi_no": customer_data["vergi_no"],
                "email": customer_data["email"],
                "telefon": customer_data["telefon"]
            }
            
            existing_customer = await self.wolvox.find_customer(search_params)
            if existing_customer:
                logger.info(f"Mevcut müşteri bulundu: {existing_customer['musteri_kodu']}")
                return existing_customer["musteri_kodu"]
            
            # Müşteri bulunamadı, yeni oluştur
            musteri_kodu = await self.wolvox.create_customer(customer_data)
            if musteri_kodu:
                logger.info(f"Yeni müşteri oluşturuldu: {musteri_kodu}")
                return musteri_kodu
            else:
                logger.error("Yeni müşteri oluşturulamadı")
                raise RuntimeError("Yeni müşteri oluşturulamadı")

        except ValueError as e:
            logger.error(f"Müşteri bulma/oluşturma doğrulama hatası: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Müşteri bulma/oluşturma hatası: {str(e)}")
            raise RuntimeError(f"Müşteri bulma/oluşturma hatası: {str(e)}")

    async def sync_product(self, stok_kodu: str) -> bool:
        """Tek bir ürünü senkronize et"""
        try:
            # Wolvox'tan ürün bilgilerini al
            product = await self.wolvox.get_product_by_code(stok_kodu)
            if not product:
                logger.error(f"Ürün bulunamadı: {stok_kodu}")
                return False
            
            # WooCommerce ürün verilerini hazırla
            woo_product = {
                "name": product["stok_adi"],
                "type": "simple",
                "regular_price": str(product["satis_fiyat1"]),
                "description": product.get("aciklama", ""),
                "short_description": product.get("aciklama", "")[:100] if product.get("aciklama") else "",
                "sku": product["stok_kodu"],
                "manage_stock": True,
                "stock_quantity": int(product["stok_miktari"]),
                "categories": [
                    {"id": product.get("kategori_kodu", 0)}
                ] if product.get("kategori_kodu") else [],
                "attributes": [
                    {
                        "name": "Marka",
                        "visible": True,
                        "options": [product.get("marka_kodu", "")]
                    }
                ] if product.get("marka_kodu") else []
            }
            
            # WooCommerce'de ürünü güncelle veya oluştur
            result = await self.woo.create_product(woo_product)
            if result:
                logger.info(f"Ürün senkronize edildi: {stok_kodu}")
                return True
            else:
                logger.error(f"Ürün senkronizasyon hatası: {stok_kodu}")
                return False
                
        except Exception as e:
            logger.error(f"Ürün senkronizasyon hatası: {str(e)}")
            return False
    
    async def sync_all_products(self, batch_size: int = 10) -> Dict[str, Any]:
        """Tüm ürünleri senkronize et"""
        try:
            offset = 0
            total_synced = 0
            total_failed = 0
            
            while True:
                # Wolvox'tan ürünleri al
                products = await self.wolvox.get_products(limit=batch_size, offset=offset)
                if not products["data"]:
                    break
                    
                # Her ürünü senkronize et
                for product in products["data"]:
                    success = await self.sync_product(product["stok_kodu"])
                    if success:
                        total_synced += 1
                    else:
                        total_failed += 1
                
                offset += batch_size
                
                # Tüm ürünler işlendiyse döngüden çık
                if offset >= products["total"]:
                    break
            
            return {
                "total_synced": total_synced,
                "total_failed": total_failed,
                "total_processed": total_synced + total_failed
            }
            
        except Exception as e:
            logger.error(f"Toplu senkronizasyon hatası: {str(e)}")
            return {
                "total_synced": total_synced,
                "total_failed": total_failed,
                "total_processed": total_synced + total_failed,
                "error": str(e)
            }
    
    async def sync_stock(self, stok_kodu: str) -> bool:
        """Stok miktarını senkronize et"""
        try:
            # Wolvox'tan güncel stok bilgisini al
            product = await self.wolvox.get_product_by_code(stok_kodu)
            if not product:
                logger.error(f"Ürün bulunamadı: {stok_kodu}")
                return False
            
            # WooCommerce'de stok miktarını güncelle
            woo_product = {
                "stock_quantity": int(product["stok_miktari"])
            }
            
            # TODO: WooCommerce ürün ID'sini bul
            # Şimdilik mock
            woo_product_id = 1
            
            result = await self.woo.update_product(woo_product_id, woo_product)
            if result:
                logger.info(f"Stok senkronize edildi: {stok_kodu}")
                return True
            else:
                logger.error(f"Stok senkronizasyon hatası: {stok_kodu}")
                return False
                
        except Exception as e:
            logger.error(f"Stok senkronizasyon hatası: {str(e)}")
            return False

    async def sync_order(self, woo_order_id: int) -> bool:
        """WooCommerce siparişini Wolvox'a aktar"""
        try:
            # WooCommerce'den sipariş bilgilerini al
            woo_order = await self.woo.get_order(woo_order_id)
            if not woo_order:
                logger.error(f"WooCommerce sipariş bulunamadı: {woo_order_id}")
                return False

            # Müşteriyi bul veya oluştur
            musteri_kodu = await self.get_or_create_customer(woo_order["customer_id"])
            if not musteri_kodu:
                logger.error(f"Müşteri bulunamadı veya oluşturulamadı: {woo_order['customer_id']}")
                return False

            # Sipariş kalemlerini hazırla
            items = []
            for item in woo_order["line_items"]:
                # Wolvox stok kodunu bul
                product = await self.wolvox.get_product_by_code(item["sku"])
                if not product:
                    logger.error(f"Ürün bulunamadı: {item['sku']}")
                    continue

                # KDV hesapla
                kdv_orani = float(product["kdv_orani"])
                birim_fiyat = float(item["price"])
                miktar = float(item["quantity"])
                tutar = birim_fiyat * miktar
                kdv_tutari = tutar * (kdv_orani / 100)
                genel_toplam = tutar + kdv_tutari

                items.append({
                    "stok_kodu": item["sku"],
                    "miktar": miktar,
                    "birim_fiyat": birim_fiyat,
                    "kdv_orani": kdv_orani,
                    "tutar": tutar,
                    "kdv_tutari": kdv_tutari,
                    "genel_toplam": genel_toplam,
                    "birim": product["birim"]
                })

            # Toplam tutarları hesapla
            toplam_tutar = sum(item["tutar"] for item in items)
            toplam_kdv = sum(item["kdv_tutari"] for item in items)
            genel_toplam = sum(item["genel_toplam"] for item in items)

            # Siparişi oluştur
            order_data = {
                "musteri_kodu": musteri_kodu,
                "toplam_tutar": toplam_tutar,
                "kdv_tutari": toplam_kdv,
                "genel_toplam": genel_toplam,
                "aciklama": f"WooCommerce Sipariş #{woo_order_id}",
                "items": items
            }

            # Wolvox'a siparişi kaydet
            siparis_no = await self.wolvox.create_order(order_data)
            if siparis_no:
                logger.info(f"Sipariş senkronize edildi: WooCommerce #{woo_order_id} -> Wolvox #{siparis_no}")
                return True
            else:
                logger.error(f"Sipariş oluşturulamadı: {woo_order_id}")
                return False

        except Exception as e:
            logger.error(f"Sipariş senkronizasyon hatası: {str(e)}")
            return False

    async def sync_pending_orders(self) -> Dict[str, Any]:
        """Bekleyen siparişleri senkronize et"""
        try:
            # WooCommerce'den bekleyen siparişleri al
            pending_orders = await self.woo.get_orders(status="processing")
            if not pending_orders:
                return {
                    "total_synced": 0,
                    "total_failed": 0,
                    "total_processed": 0
                }

            total_synced = 0
            total_failed = 0

            # Her siparişi senkronize et
            for order in pending_orders:
                success = await self.sync_order(order["id"])
                if success:
                    # Siparişi tamamlandı olarak işaretle
                    await self.woo.update_order(order["id"], {"status": "completed"})
                    total_synced += 1
                else:
                    total_failed += 1

            return {
                "total_synced": total_synced,
                "total_failed": total_failed,
                "total_processed": total_synced + total_failed
            }

        except Exception as e:
            logger.error(f"Toplu sipariş senkronizasyon hatası: {str(e)}")
            return {
                "total_synced": 0,
                "total_failed": 0,
                "total_processed": 0,
                "error": str(e)
            }

# Servis örneği
sync_service = SyncService()
