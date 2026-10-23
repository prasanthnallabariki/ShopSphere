import pytest
from unittest.mock import patch

from orders.repositories.order_repository import OrderRepository

@pytest.mark.django_db
def test_create_order_with_mocking():
    with patch.object(OrderRepository, "create_order_item") as mock_create:
        mock_create.return_value = "Fake Order Item"
        result= OrderRepository.create_order_item(order=None, product= None, quantity=2, price=100)
        assert result == "Fake Order Item"
        mock_create.assert_called_once()
