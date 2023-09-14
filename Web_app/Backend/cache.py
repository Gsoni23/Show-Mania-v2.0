from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://127.0.0.1:6379/0'})