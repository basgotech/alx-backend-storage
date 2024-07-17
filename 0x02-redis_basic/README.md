# alx-backend-storage

## 0x02-redis_basic

This repository contains solutions to tasks involving Redis as a caching system. Below are the tasks and their corresponding solutions:

### Tasks

#### 0. Writing strings to Redis

Create a `Cache` class. In the `__init__` method, store an instance of the Redis client as a private variable named `_redis` (using `redis.Redis()`) and flush the instance using `flushdb`.

Create a `store` method that takes a `data` argument and returns a string. The method should generate a random key (e.g., using `uuid`), store the input data in Redis using the random key, and return the key.

Type-annotate `store` correctly. Remember that `data` can be a `str`, `bytes`, `int`, or `float`.

**File:** `exercise.py`

```python
#!/usr/bin/env python3
"""
Main file
"""
import redis

Cache = __import__('exercise').Cache

cache = Cache()

data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))
