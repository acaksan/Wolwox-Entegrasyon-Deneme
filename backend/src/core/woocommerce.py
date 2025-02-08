from src.core.settings import get_settings
from woocommerce import API

settings = get_settings()

def get_woocommerce_client():
    return API(
        url=settings.WOOCOMMERCE_URL,
        consumer_key=settings.WOOCOMMERCE_KEY,
        consumer_secret=settings.WOOCOMMERCE_SECRET,
        version=settings.WOOCOMMERCE_API_VERSION,
        verify_ssl=settings.WOOCOMMERCE_VERIFY_SSL
    ) 