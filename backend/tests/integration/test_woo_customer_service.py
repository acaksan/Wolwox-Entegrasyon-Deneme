from datetime import datetime

import pytest


@pytest.mark.asyncio
class TestWooCommerceCustomerService:
    async def test_customer_create_event(self, woo_customer_service):
        """Müşteri oluşturma eventi testi"""
        received_events = []
        
        async def handle_customer_create(data: dict):
            received_events.append(data)
            
        woo_customer_service.event_service.subscribe(
            "customer_created",
            handle_customer_create
        )
        
        customer_data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
        
        customer = await woo_customer_service.create_customer(customer_data)
        
        assert len(received_events) == 1
        assert received_events[0]["customer_id"] == customer["id"]
        
    async def test_customer_update_event(self, woo_customer_service):
        """Müşteri güncelleme eventi testi"""
        received_events = []
        
        async def handle_customer_update(data: dict):
            received_events.append(data)
            
        woo_customer_service.event_service.subscribe(
            "customer_updated",
            handle_customer_update
        )
        
        update_data = {
            "first_name": "Updated",
            "phone": "1234567890"
        }
        
        await woo_customer_service.update_customer(123, update_data)
        
        assert len(received_events) == 1
        assert received_events[0]["customer_id"] == 123
        assert received_events[0]["changes"] == update_data
        
    async def test_get_customer_orders(self, woo_customer_service):
        """Müşteri siparişleri testi"""
        orders = await woo_customer_service.get_customer_orders(123)
        
        assert isinstance(orders, list)
        for order in orders:
            assert order["customer_id"] == 123 