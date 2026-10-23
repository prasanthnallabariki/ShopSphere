from django.core.cache import cache

PRODUCT_CACHE_VERSION_KEY = "products:cache_version"

def get_product_cache_version():
    return cache.get(PRODUCT_CACHE_VERSION_KEY,1)

def invalidate_product_cache():
    current_version = cache.get(PRODUCT_CACHE_VERSION_KEY)
    if current_version is None:
        cache.set(PRODUCT_CACHE_VERSION_KEY,2)
    else:
        cache.incr(PRODUCT_CACHE_VERSION_KEY)

def get_product_cache_key(request):
    version = get_product_cache_version()
    params = request.query_params.copy()
    normalized_params = sorted(params.items())
    query_string = "&".join(f"{key}={value}" for key, value in normalized_params)
    return f"products:list:v{version}:{query_string}"