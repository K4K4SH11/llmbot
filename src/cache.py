import redis

class RedisCache:
    def __init__(self, config):
        self.client = redis.Redis(
            host=config["host"],
            port=config["port"],
            db=config["db"],
            decode_responses=True
        )

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value, ttl=3600):
        self.client.setex(key, ttl, value)