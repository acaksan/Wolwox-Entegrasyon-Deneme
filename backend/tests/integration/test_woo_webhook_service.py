from datetime import datetime

import pytest


@pytest.mark.asyncio
class TestWooCommerceWebhookService:
    async def test_create_webhook_event(self, woo_webhook_service):
        """Webhook oluşturma eventi testi"""
        received_events = []
        
        async def handle_webhook_create(data: dict):
            received_events.append(data)
            
        woo_webhook_service.event_service.subscribe(
            "webhook_created",
            handle_webhook_create
        )
        
        webhook_data = {
            "name": "Order created",
            "topic": "order.created",
            "delivery_url": "https://webhook.site/123",
            "status": "active"
        }
        
        webhook = await woo_webhook_service.create_webhook(webhook_data)
        
        assert len(received_events) == 1
        assert received_events[0]["webhook_id"] == webhook["id"]
        
    async def test_update_webhook_event(self, woo_webhook_service):
        """Webhook güncelleme eventi testi"""
        received_events = []
        
        async def handle_webhook_update(data: dict):
            received_events.append(data)
            
        woo_webhook_service.event_service.subscribe(
            "webhook_updated",
            handle_webhook_update
        )
        
        update_data = {
            "status": "paused",
            "secret": "yeni_secret"
        }
        
        await woo_webhook_service.update_webhook(1, update_data)
        
        assert len(received_events) == 1
        assert received_events[0]["webhook_id"] == 1
        assert received_events[0]["changes"] == update_data
        
    async def test_delete_webhook_event(self, woo_webhook_service):
        """Webhook silme eventi testi"""
        received_events = []
        
        async def handle_webhook_delete(data: dict):
            received_events.append(data)
            
        woo_webhook_service.event_service.subscribe(
            "webhook_deleted",
            handle_webhook_delete
        )
        
        await woo_webhook_service.delete_webhook(1)
        
        assert len(received_events) == 1
        assert received_events[0]["webhook_id"] == 1
        
    async def test_get_webhooks(self, woo_webhook_service):
        """Webhook listesi testi"""
        webhooks = await woo_webhook_service.get_webhooks()
        
        assert isinstance(webhooks, list)
        for webhook in webhooks:
            assert "id" in webhook
            assert "name" in webhook
            assert "status" in webhook 