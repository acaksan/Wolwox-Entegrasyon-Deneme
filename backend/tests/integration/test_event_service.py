from datetime import datetime, timedelta

import pytest
from services.event_service import EventService


@pytest.mark.asyncio
class TestEventService:
    @pytest.fixture
    async def event_service(self):
        return EventService()
        
    async def test_event_publish_subscribe(self, event_service):
        """Event yayınlama ve dinleme testi"""
        received_data = []
        
        # Test event handler
        async def test_handler(data: dict):
            received_data.append(data)
            
        # Subscribe
        event_service.subscribe("test_event", test_handler)
        
        # Test verisi
        test_data = {"message": "test", "timestamp": datetime.now().isoformat()}
        
        # Event yayınla
        await event_service.publish("test_event", test_data)
        
        # Kontroller
        assert len(received_data) == 1
        assert received_data[0]["message"] == "test"
        
    async def test_multiple_subscribers(self, event_service):
        """Çoklu subscriber testi"""
        results = []
        
        # İki farklı handler
        async def handler1(data: dict):
            results.append(f"handler1_{data['id']}")
            
        async def handler2(data: dict):
            results.append(f"handler2_{data['id']}")
            
        # Her iki handler'ı da subscribe et
        event_service.subscribe("test_event", handler1)
        event_service.subscribe("test_event", handler2)
        
        # Event yayınla
        await event_service.publish("test_event", {"id": 123})
        
        # Her iki handler da çalışmalı
        assert len(results) == 2
        assert "handler1_123" in results
        assert "handler2_123" in results
        
    async def test_event_history(self, event_service):
        """Event geçmişi testi"""
        # Events yayınla
        await event_service.publish("event_type_1", {"data": "test1"})
        await event_service.publish("event_type_2", {"data": "test2"})
        await event_service.publish("event_type_1", {"data": "test3"})
        
        # History'yi kontrol et
        history = event_service.get_event_history()  # sync versiyon kullan
        assert len(history) == 3
        assert history[0]["type"] == "event_type_1"
        assert history[1]["type"] == "event_type_2"
        
    async def test_error_handling(self, event_service):
        """Hata yönetimi testi"""
        async def error_handler(data):
            raise Exception("Test error")
            
        event_service.subscribe("test_event", error_handler)
        await event_service.publish("test_event", {"data": "test"})
        
        history = event_service.get_event_history()  # sync versiyon kullan
        assert len(history) == 1 