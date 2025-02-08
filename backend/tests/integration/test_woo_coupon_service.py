from datetime import datetime

import pytest


@pytest.mark.asyncio
class TestWooCommerceCouponService:
    async def test_create_coupon_event(self, woo_coupon_service):
        """Kupon oluşturma eventi testi"""
        received_events = []
        
        async def handle_coupon_create(data: dict):
            received_events.append(data)
            
        woo_coupon_service.event_service.subscribe(
            "coupon_created",
            handle_coupon_create
        )
        
        coupon_data = {
            "code": "TEST20",
            "discount_type": "percent",
            "amount": "20",
            "individual_use": True,
            "usage_limit": 100
        }
        
        coupon = await woo_coupon_service.create_coupon(coupon_data)
        
        assert len(received_events) == 1
        assert received_events[0]["coupon_id"] == coupon["id"]
        assert received_events[0]["coupon_code"] == "TEST20"
        
    async def test_update_coupon_event(self, woo_coupon_service):
        """Kupon güncelleme eventi testi"""
        received_events = []
        
        async def handle_coupon_update(data: dict):
            received_events.append(data)
            
        woo_coupon_service.event_service.subscribe(
            "coupon_updated",
            handle_coupon_update
        )
        
        update_data = {
            "amount": "25",
            "usage_limit": 200
        }
        
        await woo_coupon_service.update_coupon(1, update_data)
        
        assert len(received_events) == 1
        assert received_events[0]["coupon_id"] == 1
        assert received_events[0]["changes"] == update_data
        
    async def test_delete_coupon_event(self, woo_coupon_service):
        """Kupon silme eventi testi"""
        received_events = []
        
        async def handle_coupon_delete(data: dict):
            received_events.append(data)
            
        woo_coupon_service.event_service.subscribe(
            "coupon_deleted",
            handle_coupon_delete
        )
        
        await woo_coupon_service.delete_coupon(1)
        
        assert len(received_events) == 1
        assert received_events[0]["coupon_id"] == 1
        
    async def test_get_coupons(self, woo_coupon_service):
        """Kupon listesi testi"""
        coupons = await woo_coupon_service.get_coupons()
        
        assert isinstance(coupons, list)
        for coupon in coupons:
            assert "id" in coupon
            assert "code" in coupon
            assert "amount" in coupon 