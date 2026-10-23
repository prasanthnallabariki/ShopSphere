import pytest
from django.contrib.auth import get_user_model
from decimal import Decimal

from catalog.models import Category, Product
from cart.models import Cart, CartItem
from cart.services.cart_service import CartService
from orders.services.order_service import OrderService

@pytest.mark.django_db
def test_adding_same_product_increase_quantity():
    User=get_user_model()
    user= User.objects.create_user(username="cart_customer", password= "Password@123")
    category= Category.objects.create(name="Cart Category")
    product= Product.objects.create(name="Cart Product", price= Decimal("100.00"), category= category, stock= 5)
    #first addition
    CartService.add_item(user=user, product_id=product.id, quantity=2)
    #second addition
    CartService.add_item(user=user, product_id=product.id, quantity=3)
    cart= Cart.objects.get(user=user)
    item= CartItem.objects.get(cart=cart, product=product)
    assert item.quantity == 5
    assert CartItem.objects.filter(cart=cart, product=product).count() == 1

@pytest.mark.django_db
def test_add_nonexistent_product():
    User=get_user_model()
    user= User.objects.create_user(username="invalid_product_user", password= "Password@123")
    with pytest.raises(Exception):
        CartService.add_item(user=user, product_id=888888, quantity=2)
