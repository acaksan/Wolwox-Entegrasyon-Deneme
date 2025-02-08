from datetime import datetime

import pytest


@pytest.mark.asyncio
class TestWooCommerceShippingService:
    async def test_create_shipping_zone_event(self, woo_shipping_service):
        """Kargo bölgesi oluşturma eventi testi"""
        received_events = []
        
        async def handle_zone_create(data: dict):
            received_events.append(data)
            
        woo_shipping_service.event_service.subscribe(
            "shipping_zone_created",
            handle_zone_create
        )
        
        zone_data = {
            "name": "Test Zone",
            "locations": [
                {
                    "type": "country",
                    "code": "TR"
                }
            ]
        }
        
        zone = await woo_shipping_service.create_shipping_zone(zone_data)
        
        assert len(received_events) == 1
        assert received_events[0]["zone_id"] == zone["id"]
        
    async def test_add_shipping_method_event(self, woo_shipping_service):
        """Kargo metodu ekleme eventi testi"""
        received_events = []
        
        async def handle_method_add(data: dict):
            received_events.append(data)
            
        woo_shipping_service.event_service.subscribe(
            "shipping_method_added",
            handle_method_add
        )
        
        method_data = {
            "method_id": "flat_rate",
            "settings": {
                "title": "Sabit Fiyat",
                "cost": "15.00"
            }
        }
        
        method = await woo_shipping_service.add_shipping_method(1, method_data)
        
        assert len(received_events) == 1
        assert received_events[0]["zone_id"] == 1
        assert received_events[0]["method_id"] == method["id"]
        
    async def test_get_shipping_zones(self, woo_shipping_service):
        """Kargo bölgeleri listeleme testi"""
        zones = await woo_shipping_service.get_shipping_zones()
        
        assert isinstance(zones, list)
        for zone in zones:
            assert "id" in zone
            assert "name" in zone 