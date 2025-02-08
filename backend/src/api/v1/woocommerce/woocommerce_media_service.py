"""WooCommerce medya servisi"""

import base64
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp
from src.core.exceptions import WooCommerceException
from src.core.settings import settings

from .base_service import BaseService

logger = logging.getLogger(__name__)

class WooCommerceMediaService(BaseService):
    """WooCommerce medya işlemleri için servis sınıfı"""
    
    def __init__(self):
        super().__init__()
        # WordPress kimlik bilgileri
        self.wp_auth = base64.b64encode(
            f"{settings.WORDPRESS_USERNAME}:{settings.WORDPRESS_PASSWORD}".encode()
        ).decode('ascii')
        self.wp_headers = {
            'Authorization': f'Basic {self.wp_auth}',
            'Content-Type': 'application/json'
        }
        self.wp_api_url = f"{settings.WOOCOMMERCE_URL}/wp-json/wp/v2"
    
    async def upload_image(
        self,
        image_path: str,
        title: Optional[str] = None,
        alt_text: Optional[str] = None,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """WordPress REST API kullanarak resim yükler"""
        try:
            path = Path(image_path)
            if not path.exists():
                raise WooCommerceException(f"Resim bulunamadı: {image_path}")
            
            # Dosya açma işlemi güvenli hale getirildi
            with open(image_path, "rb") as file:
                data = aiohttp.FormData()
                data.add_field("file", file, filename=path.name)
                
                if title:
                    data.add_field("title", title)
                if alt_text:
                    data.add_field("alt_text", alt_text)
                if caption:
                    data.add_field("caption", caption)
                
                # WordPress REST API'ye yükle
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.wp_api_url}/media",
                        headers={'Authorization': f'Basic {self.wp_auth}'},
                        data=data
                    ) as response:
                        if response.status != 201:
                            text = await response.text()
                            logger.error(f"❌ Resim yükleme hatası: HTTP {response.status} - {text}")
                            raise WooCommerceException(f"Resim yükleme hatası: HTTP {response.status} - {text}")
                        
                        result = await response.json()
                        logger.info(f"✅ Resim yüklendi: {result.get('source_url')}")
                        return result
                    
        except Exception as e:
            logger.error(f"❌ Resim yükleme hatası: {str(e)}")
            raise WooCommerceException(f"Resim yükleme hatası: {str(e)}")
    
    async def delete_image(self, image_id: int, force: bool = False) -> bool:
        """WordPress REST API kullanarak resim siler"""
        try:
            params = {"force": "true"} if force else {}
            
            # WordPress REST API'den sil
            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    f"{self.wp_api_url}/media/{image_id}",
                    headers={'Authorization': f'Basic {self.wp_auth}'},
                    params=params
                ) as response:
                    if response.status not in (200, 204):
                        text = await response.text()
                        raise WooCommerceException(
                            f"Resim silme hatası: HTTP {response.status} - {text}"
                        )
                    
                    logger.info(f"✅ Resim silindi: {image_id}")
                    return True
            
        except Exception as e:
            logger.error(f"❌ Resim silme hatası: {str(e)}")
            raise WooCommerceException(f"Resim silme hatası: {str(e)}")

# Singleton instance
woo_media_service = WooCommerceMediaService()

__all__ = ['WooCommerceMediaService', 'woo_media_service']
