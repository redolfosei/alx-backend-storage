#!/usr/bin/env python3
""" Function which implements an expiring web cache tracker """
import requests
import time
from functools import wraps
from typing import Dict

cache: Dict[str, str] = {}

def get_page(url: str) -> str:
    if url in cache:
        print(f"Retrieving data from cache: {url}")
        return cache[url]
    else:
        print(f"Retrieving data from web: {url}")
        response = requests.get(url)
        result = response.text
        cache[url] = result
        return result
