from django.core.cache import cache

def test_django_redis_cache():
    cache.set("shopsphere:test", "hello", timeout=60)
    assert cache.get("shopsphere:test") == "hello"
    cache.delete("shopsphere:test")
    assert cache.get("shopsphere:test") is None