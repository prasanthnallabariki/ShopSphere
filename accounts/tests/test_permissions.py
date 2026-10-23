import pytest
from django.contrib.auth import get_user_model

from accounts.permissions import IsCustomer, IsSeller, IsAdmin, IsSellerOrAdmin

@pytest.mark.django_db
def test_customer_permission():
    User= get_user_model()
    user= User.objects.create_user(username="customer", password="Password@123", role= User.Role.CUSTOMER)
    assert IsCustomer().has_permission(type("Request", (), {"user":user})(), None)
    assert not IsSeller().has_permission(type("Request", (), {"user":user})(), None)
    assert not IsAdmin().has_permission(type("Request", (), {"user":user})(), None)

@pytest.mark.django_db
def test_seller_permission():
    User= get_user_model()
    user= User.objects.create_user(username="seller", password="Password@123", role= User.Role.SELLER)
    assert IsSeller().has_permission(type("Request", (), {"user":user})(), None)
    assert IsSellerOrAdmin().has_permission(type("Request", (), {"user":user})(), None)
    assert not IsAdmin().has_permission(type("Request", (), {"user":user})(), None)

@pytest.mark.django_db
def test_admin_permission():
    User= get_user_model()
    user= User.objects.create_user(username="admin", password="Password@123", role= User.Role.ADMIN)
    assert IsAdmin().has_permission(type("Request", (), {"user":user})(), None)
    assert IsSellerOrAdmin().has_permission(type("Request", (), {"user":user})(), None)
