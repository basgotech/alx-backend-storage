#!/usr/bin/env python3

import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union

"""
This module implements a caching system using Redis as the backend.
It provides decorators for counting function calls and tracking function call history,
as well as a class `Cache` that wraps Redis operations with additional functionality.
"""

def count_calls(method: Callable) -> Callable:
    """
    Decorator that increments a counter in Redis each time the decorated method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with call counting functionality.
    """
    @wraps(method)
    def mystic(self, *args, **kwargs) -> Any:
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return mystic

def call_history(method: Callable) -> Callable:
    """
    Decorator that logs the inputs and outputs of the decorated method in Redis.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with call history logging functionality.
    """
    @wraps(method)
    def mystic(self, *args, **kwargs) -> Any:
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return mystic

def replay(met: Callable) -> None:
    """
    Displays the call history of a given function, including the number of times it was called,
    the arguments it was called with, and the results it returned.

    Args:
        fn (Callable): The function whose call history is to be displayed.
    """
    if met is None or not hasattr(met, '__self__'):
        return
    rad = getattr(met.__self__, '_redis', None)
    if not isinstance(rad, redis.Redis):
        return
    name_getter = met.__qualname__
    key_getter = '{}:inputs'.format(name_getter)
    key_in = '{}:outputs'.format(name_getter)
    fxn_call_count = 0
    if rad.exists(name_getter) != 0:
        fxn_call_count = int(rad.get(name_getter))
    print('{} was called {} times:'.format(name_getter, fxn_call_count))
    setter = rad.lrange(key_getter, 0, -1)
    fxn_outputs = rad.lrange(key_in, 0, -1)
    for f_setter, fxn_output in zip(setter, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            name_getter,
            f_setter.decode("utf-8"),
            fxn_output,
        ))

class Cache:
    """
    A caching class that uses Redis to store and retrieve data.
    Provides methods to store data with automatic key generation, and to retrieve data
    with optional type conversion.

    Methods:
        store(data): Stores data in Redis with a generated UUID key.
        get(key, fn): Retrieves data from Redis, optionally converting it with a provided function.
        get_str(key): Retrieves data from Redis and decodes it as a string.
        get_int(key): Retrieves data from Redis and converts it to an integer.
    """
    
    def __init__(self) -> None:
        """
        Initializes the Cache instance, setting up the Redis connection and flushing the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis with a generated UUID key and logs the call history and count.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The generated UUID key for the stored data.
        """
        key_holder = str(uuid.uuid4())
        self._redis.set(key_holder, data)
        return key_holder

    def get(self, key: str, met: Callable = None) -> Union[str, bytes, int, float]:
        """
        Retrieves data from Redis, optionally converting it with a provided function.

        Args:
            key (str): The key of the data to be retrieved.
            fn (Callable, optional): A function to convert the retrieved data.

        Returns:
            Union[str, bytes, int, float]: The retrieved data, optionally converted.
        """
        holder = self._redis.get(key)
        return met(holder) if met is not None else holder

    def get_str(self, key: str) -> str:
        """
        Retrieves data from Redis and decodes it as a string.

        Args:
            key (str): The key of the data to be retrieved.

        Returns:
            str: The retrieved data decoded as a string.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves data from Redis and converts it to an integer.

        Args:
            key (str): The key of the data to be retrieved.

        Returns:
            int: The retrieved data converted to an integer.
        """
        return self.get(key, lambda x: int(x))
