from datetime import datetime

import pytest


@pytest.mark.asyncio
class TestWooCommerceOrderService:
    async def test_order_create_event(self, woo_order_service):
        """Sipariş oluşturma eventi testi"""
        received_events = []
        
        async def handle_order_create(data: dict):
            received_events.append(data)
            
        woo_order_service.event_service.subscribe(
            "order_created",
            handle_order_create
        )
        
        order_data = {
            "customer_id": 1,
            "payment_method": "bacs",
            "line_items": [
                {
                    "product_id": 123,
                    "quantity": 2
                }
            ]
        }
        
        order = await woo_order_service.create_order(order_data)
        
        assert len(received_events) == 1
        assert received_events[0]["order_id"] == order["id"]
        
    async def test_order_status_change_event(self, woo_order_service):
        """Sipariş durum değişikliği eventi testi"""
        received_events = []
        
        async def handle_status_change(data: dict):
            received_events.append(data)
            
        woo_order_service.event_service.subscribe(
            "order_status_changed",
            handle_status_change
        )
        
        await woo_order_service.update_status(
            order_id=123,
            status="processing",
            note="Sipariş işleme alındı"
        )
        
        assert len(received_events) == 1
        assert received_events[0]["order_id"] == 123
        assert received_events[0]["new_status"] == "processing"
        
    async def test_order_completion_event(self, woo_order_service):
        """Sipariş tamamlama eventi testi"""
        received_events = []
        
        async def handle_completion(data: dict):
            received_events.append(data)
            
        woo_order_service.event_service.subscribe(
            "order_completed",
            handle_completion
        )
        
        await woo_order_service.complete_order(123)
        
        assert len(received_events) == 1
        assert received_events[0]["order_id"] == 123
        assert "completion_time" in received_events[0] 