#!/usr/bin/env python3

import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union

"""
This module implements a caching system
using Redis as the backend.
"""

def count_calls(func: Callable) -> Callable:
    """
    Decorator that increments a counter in Redis each time the decorated method is called.

    Args:
        func (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with call counting functionality.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> Any:
        if isinstance(self.redis_instance, redis.Redis):
            self.redis_instance.incr(func.__qualname__)
        return func(self, *args, **kwargs)
    return wrapper

def call_history(func: Callable) -> Callable:
    """
    Decorator that logs the inputs and outputs of the decorated method in Redis.

    Args:
        func (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with call history logging functionality.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> Any:
        input_key = '{}:inputs'.format(func.__qualname__)
        output_key = '{}:outputs'.format(func.__qualname__)
        if isinstance(self.redis_instance, redis.Redis):
            self.redis_instance.rpush(input_key, str(args))
        result = func(self, *args, **kwargs)
        if isinstance(self.redis_instance, redis.Redis):
            self.redis_instance.rpush(output_key, result)
        return result
    return wrapper

def replay(function: Callable) -> None:
    """
    Displays the call history of a given function, including the number of times it was called,
    the arguments it was called with, and the results it returned.

    Args:
        function (Callable): The function whose call history is to be displayed.
    """
    if function is None or not hasattr(function, '__self__'):
        return
    redis_instance = getattr(function.__self__, 'redis_instance', None)
    if not isinstance(redis_instance, redis.Redis):
        return
    function_name = function.__qualname__
    input_key = '{}:inputs'.format(function_name)
    output_key = '{}:outputs'.format(function_name)
    call_count = 0
    if redis_instance.exists(function_name) != 0:
        call_count = int(redis_instance.get(function_name))
    print('{} was called {} times:'.format(function_name, call_count))
    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)
    for input_value, output_value in zip(inputs, outputs):
        print('{}(*{}) -> {}'.format(
            function_name,
            input_value.decode("utf-8"),
            output_value,
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
        self.redis_instance = redis.Redis()
        self.redis_instance.flushdb(True)

    @call_history
    @count_calls
    def store(self, value: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis with a generated UUID key and logs the call history and count.

        Args:
            value (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The generated UUID key for the stored data.
        """
        key = str(uuid.uuid4())
        self.redis_instance.set(key, value)
        return key

    def get(self, key: str, transform: Callable = None) -> Union[str, bytes, int, float]:
        """
        Retrieves data from Redis, optionally converting it with a provided function.

        Args:
            key (str): The key of the data to be retrieved.
            transform (Callable, optional): A function to convert the retrieved data.

        Returns:
            Union[str, bytes, int, float]: The retrieved data, optionally converted.
        """
        value = self.redis_instance.get(key)
        return transform(value) if transform is not None else value

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
