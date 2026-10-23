import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings

from catalog.models import Category, Product
from orders.models import Order
from orders.tasks import process_order_notification

from unittest.mock import patch

@pytest.mark.django_db
@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
def test_order_notification_sends_email():
    User=get_user_model()
    user= User.objects.create_user(username="testuser", password="Password@123", email="testuser@example.com")
    order= Order.objects.create(user=user, total_amount=Decimal("100.00"))
    result= process_order_notification(order.id)

    assert result == f"Email sent for order {order.id}"
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ["testuser@example.com"]
    assert f"#{order.id}" in mail.outbox[0].subject

@pytest.mark.django_db
def test_order_notification_retries_on_timeout():
    User= get_user_model()
    user= User.objects.create_user(username="testuser", password="Password@123", email="testuser@example.com")
    order= Order.objects.create(user=user, total_amount=Decimal("100.00"))
    with patch("orders.tasks.send_mail", side_effect= TimeoutError("Email server timed out")):
        with patch("orders.tasks.process_order_notification.retry", side_effect=Exception("Retry requested"), ) as mock_retry:
            with pytest.raises(Exception, match="Retry requested"):
                process_order_notification.run(order.id)
            mock_retry.assert_called_once()
