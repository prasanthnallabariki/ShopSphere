import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from catalog.models import Category, Product
from cart.models import Cart, CartItem
from decimal import Decimal


@pytest.mark.django_db
def test_get_nonexistent_order_returns_404():
    client= APIClient()
    from django.contrib.auth import get_user_model
    User= get_user_model()
    user= User.objects.create_user(username="NonexistentOrderUser", password="Password@123")
    client.force_authenticate(user=user)
    response= client.get("/api/orders/89899/")
    assert response.status_code == 404

@pytest.mark.django_db
def test_user_cannot_access_other_users_orders():
    User= get_user_model()
    user1= User.objects.create_user(username="user1", password="Password@123")
    user2= User.objects.create_user(username="user2", password="Password@123")
    
    category= Category.objects.create(name="user1Category")
    product= Product.objects.create(name="user1Product", price= Decimal("100.00"), category= category, stock=5)
    cart= Cart.objects.create(user=user1)
    cart_item= CartItem.objects.create(cart=cart, product= product, quantity=2)
    client1= APIClient()
    client1.force_authenticate(user=user1)
    response= client1.post("/api/orders/checkout/", format="json")
    assert response.status_code == 201
    order_id= response.data["id"]
    client2= APIClient()
    client2.force_authenticate(user=user2)
    response= client2.get(f"/api/orders/{order_id}/")
    assert response.status_code == 404
        