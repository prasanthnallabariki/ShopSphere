from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest

@pytest.mark.django_db
def test_order_history_requires_authentication():
    client= APIClient()
    response= client.get("/api/orders/")
    assert response.status_code == 401

@pytest.mark.django_db
def test_authenticated_user_can_view_empty_order_history():
    User= get_user_model()
    user= User.objects.create_user(username= "testuser", password="Password@123")
    client= APIClient()
    client.force_authenticate(user=user)
    response= client.get("/api/orders/")
    assert response.status_code == 200
    assert response.data["count"] == 0
    assert response.data["results"] == []
