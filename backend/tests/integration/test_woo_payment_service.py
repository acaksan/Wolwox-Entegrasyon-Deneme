from datetime import datetime

import pytest


@pytest.mark.asyncio
class TestWooCommercePaymentService:
    async def test_process_payment_event(self, woo_payment_service):
        """Ödeme işlemi eventi testi"""
        received_events = []
        
        async def handle_payment_process(data: dict):
            received_events.append(data)
            
        woo_payment_service.event_service.subscribe(
            "payment_processed",
            handle_payment_process
        )
        
        payment_data = {
            "method": "bacs",
            "title": "Banka Havalesi",
            "transaction_id": "TRX123"
        }
        
        result = await woo_payment_service.process_payment(1, payment_data)
        
        assert len(received_events) == 1
        assert received_events[0]["order_id"] == 1
        assert received_events[0]["payment_data"] == payment_data
        
    async def test_refund_payment_event(self, woo_payment_service):
        """Ödeme iadesi eventi testi"""
        received_events = []
        
        async def handle_refund(data: dict):
            received_events.append(data)
            
        woo_payment_service.event_service.subscribe(
            "payment_refunded",
            handle_refund
        )
        
        refund_data = {
            "amount": "50.00",
            "reason": "Müşteri talebi"
        }
        
        refund = await woo_payment_service.refund_payment(1, refund_data)
        
        assert len(received_events) == 1
        assert received_events[0]["order_id"] == 1
        assert received_events[0]["refund_data"] == refund_data
        
    async def test_get_payment_methods(self, woo_payment_service):
        """Ödeme yöntemleri testi"""
        methods = await woo_payment_service.get_payment_methods()
        
        assert isinstance(methods, list)
        for method in methods:
            assert method["enabled"] is True
            assert "id" in method
            assert "title" in method 