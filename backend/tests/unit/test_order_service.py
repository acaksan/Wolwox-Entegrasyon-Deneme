from unittest.mock import Mock, patch

import pytest
from services.order_service import OrderService


@pytest.mark.asyncio
async def test_process_order():
    # Arrange
    repository = Mock()
    event_bus = Mock()
    service = OrderService(repository, event_bus)
    
    order_data = {"customer_id": 1}
    
    # Act
    result = await service.process_order(order_data)
    
    # Assert
    repository.create_order.assert_called_once_with(order_data)
    event_bus.publish.assert_called_once() 