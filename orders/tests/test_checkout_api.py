import pytest
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from catalog.models import Category, Product
from cart.models import Cart, CartItem
from orders.models import Order

@pytest.mark.django_db
def test_checkout_api_success():
    User= get_user_model()
    user= User.objects.create_user(username="Api_customer", password="Password@123")
    category= Category.objects.create(name="ApiCategory")
    product= Product.objects.create(name="API Product", price= Decimal("100.00"), category= category, stock=5)
    cart= Cart.objects.create(user=user)
    cart_item= CartItem.objects.create(cart=cart, product= product, quantity=2)
    client= APIClient()
    client.force_authenticate(user=user)
    response= client.post("/api/orders/checkout/", format="json")

    assert response.status_code == 201
    assert response.data["status"] == "PENDING"
    assert response.data["total_amount"] == "200.00"
    assert Order.objects.filter(user=user).count() == 1
    product.refresh_from_db()
    assert product.stock == 3
    cart.refresh_from_db()
    assert cart.items.count() == 0

#testing unauthenticated checout

@pytest.mark.django_db
def test_checkout_api_requires_authentication():
    client= APIClient()
    response= client.post("/api/orders/checkout/", format="json")

    assert response.status_code == 401