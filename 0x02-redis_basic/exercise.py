#!/usr/bin/env python3
""" Writing strings to Redis
Reading from Redis and recovering original type,
Incrementing values, storing lists, retrieving lists
"""
import redis
from typing import Union, Optional, Callable
from uuid import uuid4
from functools import wraps


def replay(func: Callable) -> None:
    """ function which defines history """
    r = redis.Redis()
    key = func.__qualname__
    _input = r.lrange("{}:inputs".format(key), 0, -1)
    _output = r.lrange("{}:outputs".format(key), 0, -1)
    if len(_input) == 1:
        print("{} was called {} {}:".format(key, len(_input), 'time'))
    else:
        print("{} was called {} {}:".format(key, len(_input), 'times'))

    for x, y in zip(_input, _output):
        print("{}(*{}) -> {}".format(key,
                                     x.decode('utf-8'),
                                     y.decode('utf-8')))


def call_history(method: Callable) -> Callable:
    """ Function which stores history of inputs and outputs of a particular
    function"""
    @wraps(method)
    def call_history_wr(self, *args, **kwargs):
        """ callhistory wrapper definition"""
        key = method.__qualname__
        input_1 = key + ":inputs"
        output_1 = key + ":outputs"
        self._redis.rpush(input_1, str(args))
        fin = method(self, *args, **kwargs)
        self._redis.rpush(output_1, str(fin))
        return fin
    return call_history_wr


def count_calls(method: Callable) -> Callable:
    """ Function decorator which  wraps count """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Function definition for wrapper """
        key = method.__qualname__
        self._redis.incr(key, 1)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """ Function definition for Class Cache """
    def __init__(self) -> None:
        """ Initializes redis client """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Stores data in redis chache
        Args:
            data (dict): data to store
        Returns:
            str: key
        """
        k = str(uuid4())
        self._redis.set(k, data)
        return k

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
        """ Function fetches data from redis cache """
        data = self._redis.get(key)
        return data if not fn else fn(data)

    def get_str(self, key: str) -> str:
        """
        Get data as string from cache
        Args:
            key (str): key
        Returns:
            str: data
        """
        d = self.get(key, lambda x: x.decode('utf-8'))
        return d

    def get_int(self, key: str) -> Union[str, bytes, int, float]:
        """
        Function gets data as integer from redis
        Args:
            key (str): key
        Returns:
            int: data
        """
        return self.get(key, int)
