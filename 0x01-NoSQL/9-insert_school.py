#!/usr/bin/env python3
"""Python function that inserts a new document
in a collection based on kwargs:

mongo_collection will be the pymongo collection object
Returns new _id
"""


import pymongo


def insert_school(mongo_collection, **kwargs):
    """inserts a new document in a collection"""
    return mongo_collection.insert(kwargs)
