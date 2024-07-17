#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """

from functools import wraps
import redis
import requests
from typing import Callable

rad_getter_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ wrapper setter """
    @wraps(method)
    def wrapper(url):  # sourcery skip: use-named-expression
        """ Wrapper for decorator """
        rad_getter_.incr(f"count:{url}")
        ht = rad_getter_.get(f"cached:{url}")
        if ht:
            return ht.decode('utf-8')
        html_code = method(url)
        rad_getter_.setex(f"cached:{url}", 10, html_code)
        return html_code

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ RUN HTML CODE """
    requests = requests.get(url)
    return requests.text
