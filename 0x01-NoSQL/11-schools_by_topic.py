#!/usr/bin/env python3
"""Python function that returns the list of school
having a specific topic:

mongo_collection will be the pymongo collection object
topic (string) will be topic searched
"""


import pymongo


def schools_by_topic(mongo_collection, topic):
    """returns the list of schools having a specific topic"""
    return mongo_collection.find({"topics": topic})
