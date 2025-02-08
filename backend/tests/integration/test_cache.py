import pytest
from services.cache_service import CacheService


@pytest.mark.integration
class TestCache:
    @pytest.fixture
    async def cache_service(self):
        service = CacheService()
        yield service
        await service.close()
    
    @pytest.mark.asyncio
    async def test_cache_operations(self, cache_service):
        # Set
        key = "test_key"
        value = {"id": 1, "name": "Test"}
        await cache_service.set(key, value, expire=60)
        
        # Get
        cached = await cache_service.get(key)
        assert cached["id"] == value["id"]
        
        # Delete
        await cache_service.delete(key)
        assert await cache_service.get(key) is None 