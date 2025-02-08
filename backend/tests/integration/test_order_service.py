from datetime import datetime
from decimal import Decimal

import pytest
from core.exceptions import ServiceException
from models.order import Order, OrderItem, OrderStatus


@pytest.fixture
async def test_order_data():
    return {
        "customer_id": 1,
        "items": [
            {
                "product_id": 123,
                "quantity": 2,
                "unit_price": 29.99
            }
        ],
        "total_amount": 59.98,
        "notes": "Test siparişi"
    }

@pytest.mark.asyncio
async def test_order_creation(woo_service, event_bus, cache, test_order_data):
    """Sipariş oluşturma testi"""
    # WooCommerce formatına çevir
    order_data = {
        "customer_id": test_order_data["customer_id"],
        "line_items": [
            {
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "price": str(item["unit_price"])  # String olarak gönder
            }
            for item in test_order_data["items"]
        ],
        "status": "pending"
    }
    
    # Sipariş oluştur
    order = await woo_service.create_order(order_data)
    
    assert order["id"] is not None
    assert order["status"] == "pending"
    assert len(order["line_items"]) == 1
    assert order["customer_id"] == test_order_data["customer_id"]
    
    # Temizlik
    await woo_service.delete_order(order["id"])

@pytest.mark.asyncio
async def test_order_status_flow(woo_service, event_bus, cache, test_order_data):
    """Sipariş durumu akışı testi"""
    # Sipariş oluştur
    order = await woo_service.create_order(test_order_data)
    
    # Durum geçişlerini test et
    status_flow = [
        OrderStatus.PROCESSING,
        OrderStatus.COMPLETED
    ]
    
    current_order = order
    for status in status_flow:
        updated = await woo_service.update_order(
            current_order["id"],
            {
                "status": status.value,
                "status_note": f"Durum güncellendi: {status.value}"
            }
        )
        assert updated["status"] == status.value
        current_order = updated
    
    # Temizlik
    await woo_service.delete_order(order["id"])

@pytest.mark.asyncio
async def test_invalid_order_status_transition(woo_service, event_bus, cache, test_order_data):
    """Geçersiz durum geçişi testi"""
    # Sipariş oluştur
    order = await woo_service.create_order(test_order_data)
    
    # Geçersiz durum geçişi dene (pending -> completed)
    with pytest.raises(ServiceException) as exc_info:
        await woo_service.update_order(
            order["id"],
            {"status": OrderStatus.COMPLETED.value}
        )
    
    assert "Invalid status transition" in str(exc_info.value)
    
    # Temizlik
    await woo_service.delete_order(order["id"])

@pytest.mark.asyncio
async def test_order_listing_and_filtering(woo_service, event_bus, cache, test_order_data):
    """Sipariş listeleme ve filtreleme testi"""
    # Test siparişleri oluştur
    orders = []
    for i in range(3):
        data = test_order_data.copy()
        data["notes"] = f"Test sipariş {i}"
        order = await woo_service.create_order(data)
        orders.append(order)
    
    # Tüm siparişleri getir
    all_orders = await woo_service.get_orders()
    assert len(all_orders) >= 3
    
    # Durum ile filtrele
    pending_orders = await woo_service.get_orders(status="pending")
    assert all(order["status"] == "pending" for order in pending_orders)
    
    # Temizlik
    for order in orders:
        await woo_service.delete_order(order["id"])

@pytest.mark.integration
async def test_create_order():
    # Test verisi
    order_item = OrderItem(
        product_id=1,
        quantity=2,
        price=Decimal("99.99")
    )
    
    order = Order(
        customer_id=1,
        items=[order_item],
        total=Decimal("199.98"),
        status=OrderStatus.PENDING
    )
    
    assert order.status == OrderStatus.PENDING
    assert len(order.items) == 1
    assert order.total == Decimal("199.98")

@pytest.mark.integration
async def test_order_status_transition():
    order = Order(
        customer_id=1,
        items=[
            OrderItem(
                product_id=1,
                quantity=1,
                price=Decimal("99.99")
            )
        ],
        total=Decimal("99.99")
    )
    
    assert order.status == OrderStatus.PENDING
    order.status = OrderStatus.PROCESSING
    assert order.status == OrderStatus.PROCESSING 