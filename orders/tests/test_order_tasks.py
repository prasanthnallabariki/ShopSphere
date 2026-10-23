import pytest
from unittest.mock import patch
from django.db import transaction

@pytest.mark.django_db(transaction=True)
def test_notification_runs_after_commit():
    with patch("orders.services.order_service.process_order_notification.delay") as mock_task:
        with transaction.atomic():
            transaction.on_commit(lambda:mock_task(16))
            mock_task.assert_not_called()
        mock_task.assert_called_once_with(16)
