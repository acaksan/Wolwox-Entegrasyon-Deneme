from datetime import datetime

import pytest


@pytest.mark.asyncio
class TestWooCommerceTaxService:
    async def test_create_tax_rate_event(self, woo_tax_service):
        """Vergi oranı oluşturma eventi testi"""
        received_events = []
        
        async def handle_tax_create(data: dict):
            received_events.append(data)
            
        woo_tax_service.event_service.subscribe(
            "tax_rate_created",
            handle_tax_create
        )
        
        tax_data = {
            "country": "TR",
            "rate": "18.00",
            "name": "KDV",
            "shipping": True
        }
        
        tax = await woo_tax_service.create_tax_rate(tax_data)
        
        assert len(received_events) == 1
        assert received_events[0]["tax_id"] == tax["id"]
        
    async def test_update_tax_rate_event(self, woo_tax_service):
        """Vergi oranı güncelleme eventi testi"""
        received_events = []
        
        async def handle_tax_update(data: dict):
            received_events.append(data)
            
        woo_tax_service.event_service.subscribe(
            "tax_rate_updated",
            handle_tax_update
        )
        
        update_data = {
            "rate": "20.00",
            "name": "Yeni KDV"
        }
        
        await woo_tax_service.update_tax_rate(1, update_data)
        
        assert len(received_events) == 1
        assert received_events[0]["tax_id"] == 1
        assert received_events[0]["changes"] == update_data
        
    async def test_get_tax_rates(self, woo_tax_service):
        """Vergi oranları listeleme testi"""
        rates = await woo_tax_service.get_tax_rates()
        
        assert isinstance(rates, list)
        for rate in rates:
            assert "id" in rate
            assert "rate" in rate
            assert "country" in rate 