"""Health check endpoint'i"""

from fastapi import APIRouter
from src.core.database import get_db_connection
from src.utils.cache import get_cache
from src.utils.logger import logger

router = APIRouter()

@router.get("")
async def health_check():
    """Sistem sağlık kontrolü"""
    health_status = {
        "status": "healthy",
        "services": {
            "database": "unknown",
            "redis": "unknown"
        }
    }

    try:
        # Veritabanı kontrolü
        db = get_db_connection()
        if db:
            health_status["services"]["database"] = "up"
            db.close()
    except Exception as e:
        logger.error(f"Database health check error: {str(e)}")
        health_status["services"]["database"] = "down"
        health_status["status"] = "unhealthy"

    try:
        # Redis kontrolü
        cache = get_cache()
        test_key = "health_check_test"
        cache.set(test_key, "test", 5)
        if cache.get(test_key) == "test":
            health_status["services"]["redis"] = "up"
        cache.delete(test_key)
    except Exception as e:
        logger.error(f"Redis health check error: {str(e)}")
        health_status["services"]["redis"] = "down"
        health_status["status"] = "unhealthy"

    return health_status