import pytest
from rest_framework.test import APIClient, APIRequestFactory
from catalog.models import Product, Category
from accounts.models import User
from django.core.cache import cache
from rest_framework.request import Request

from catalog.cache import get_product_cache_key, get_product_cache_version, invalidate_product_cache

@pytest.mark.django_db
def test_product_list_cache_hit():
    cache.clear()
    user = User.objects.create_user(username="test user", password="testpassword")
    category = Category.objects.create(name= "test category")
    product = Product.objects.create(name= "test product", price= 12, category= category, stock=4)
    client = APIClient()
    client.force_authenticate(user=user)
    response1 = client.get("/api/catalog/products/")
    assert response1.status_code == 200
    response2 = client.get("/api/catalog/products/")
    assert response2.status_code == 200
    assert response1.data == response2.data

@pytest.mark.django_db
def test_product_cache_version_increments():
    cache.delete("products:cache_version")
    version_before = get_product_cache_version()
    invalidate_product_cache()
    version_after = get_product_cache_version()
    assert version_after > version_before

@pytest.mark.django_db
def test_product_cache_key_normalizes_query_parameter_order():
    factory = APIRequestFactory()
    request1 = Request(factory.get("/api/catalog/products/?page=1&limit=5"))
    request2 = Request(factory.get("/api/catalog/products/?limit=5&page=1"))
    key1 = get_product_cache_key(request1)
    key2 = get_product_cache_key(request2)
    assert key1 == key2