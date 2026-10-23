import pytest
from django.contrib.auth import get_user_model
from decimal import Decimal
from rest_framework.exceptions import ValidationError

from catalog.models import Category, Product
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from orders.services.order_service import OrderService

from unittest.mock import patch


@pytest.mark.django_db(transaction= True)
def test_checkout_creates_order_and_updates_stock():
    User= get_user_model()
    user= User.objects.create_user(username="testuser", password="Password@123", email="testuser@example.com")
    category= Category.objects.create(name="TestCategory")
    product= Product.objects.create(name="Test Product", price= Decimal("50.00"), category= category, stock=10)
    cart= Cart.objects.create(user=user)
    cart_item= CartItem.objects.create(cart=cart, product=product, quantity=2)
    with patch("orders.services.order_service.process_order_notification.delay") as mock_task:
        order= OrderService.checkout(user)

        assert Order.objects.filter(id=order.id).exists()
        assert order.total_amount == Decimal("100.00")
        order_item= OrderItem.objects.get(order=order)
        assert order_item.quantity == 2
        assert order_item.price == Decimal("50.00")
        product.refresh_from_db()
        assert product.stock == 8
        assert cart.items.count() == 0
        mock_task.assert_called_once_with(order.id)

@pytest.mark.django_db
def test_checkout_rejects_insufficient_stock():
    User= get_user_model()
    user= User.objects.create_user(username="testuser", password="Password@123")
    category= Category.objects.create(name="TestCategory")
    product= Product.objects.create(name="Test product", price= Decimal("0.00"), category= category, stock= 1)
    cart= Cart.objects.create(user=user)
    cart_item= CartItem.objects.create(cart=cart, product= product, quantity=3)
    with pytest.raises(ValidationError):
        OrderService.checkout(user=user)

    product.refresh_from_db()
    assert product.stock == 1
    assert Order.objects.filter(user=user).count()== 0
    assert CartItem.objects.filter(pk=cart_item.pk).exists()

@pytest.mark.django_db
def test_checkout_rolls_back_when_order_item_creation_fails(monkeypatch):
    User= get_user_model()
    user= User.objects.create_user(username="rollbackcustomer", password="Password@123")
    category= Category.objects.create(name="RollbackCategory")
    product= Product.objects.create(name="Rollback Product", price= Decimal("0.00"), category= category, stock= 5)
    cart= Cart.objects.create(user=user)
    cart_item= CartItem.objects.create(cart=cart, product= product, quantity=3)
    from orders.repositories.order_repository import OrderRepository
    def fail_order_item_creation(*args, **kwargs):
        raise RuntimeError("Simulated database failure")
    monkeypatch.setattr(OrderRepository, "create_order_item", staticmethod(fail_order_item_creation))
    with pytest.raises(RuntimeError):
        OrderService.checkout(user=user)

    assert Order.objects.filter(user=user).count() == 0
    product.refresh_from_db()
    assert product.stock == 5

    cart.refresh_from_db()
    assert cart.items.count() == 1

@pytest.mark.django_db
def test_checkout_rejects_empty_cart():
    User=get_user_model()
    user= User.objects.create_user(username="empty_cart_user", password= "Password@123")
    cart= Cart.objects.create(user=user)
    with pytest.raises(ValidationError):
        OrderService.checkout(user=user)
    assert Order.objects.filter(user=user).count() == 0

@pytest.mark.django_db
def test_checkout_rejects_out_of_stock_product():
    User=get_user_model()
    user= User.objects.create_user(username="empty_cart_user", password= "Password@123")
    category= Category.objects.create(name="Out of Stock Category")
    product= Product.objects.create(name="Out of Stock Product", price= Decimal("50.00"), category= category, stock= 0)
    cart= Cart.objects.create(user=user)
    cart_item= CartItem.objects.create(cart=cart, product=product, quantity=1)
    with pytest.raises(ValidationError):
        OrderService.checkout(user=user)
    assert Order.objects.filter(user=user).count() == 0
    product.refresh_from_db()
    assert product.stock == 0

@pytest.mark.django_db
def test_checkout_all_available_stock():
    User=get_user_model()
    user= User.objects.create_user(username="exact_stock_user", password= "Password@123")
    category= Category.objects.create(name="Exact Stock Category")
    product= Product.objects.create(name="Exact Stock Product", price= Decimal("100.00"), category= category, stock= 5)
    cart= Cart.objects.create(user=user)
    cart_item= CartItem.objects.create(cart=cart, product=product, quantity=5)
    order= OrderService.checkout(user=user)
    assert order.total_amount == Decimal("500.00")
    product.refresh_from_db()
    assert product.stock == 0
