#!/usr/bin/env python3
"""
web cache and tracker
"""

import requests
import redis
from functools import wraps
from typing import Callable

# Connect to Redis server
r = redis.Redis()

def cache_page(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(url: str) -> str:
        # Increment the count for the URL
        r.incr(f"count:{url}")

        # Check if the URL content is cached
        cached_content = r.get(f"cached:{url}")
        if cached_content:
            return cached_content.decode('utf-8')

        # If not cached, fetch and cache it
        content = func(url)
        r.setex(f"cached:{url}", 10, content)  # Cache for 10 seconds
        return content
    return wrapper

@cache_page
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Test the function with a slow response URL
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
    print(get_page(url))
