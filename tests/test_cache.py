import pytest
from src.cache import RedisCache

def test_cache_set_get():
    cache = RedisCache({"host": "localhost", "port": 6379, "db": 0})
    cache.set("test_key", "test_value", ttl=10)
    assert cache.get("test_key") == "test_value"