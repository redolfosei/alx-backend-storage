#!/usr/bin/env python3
"""
Python script for sorting scores
"""


def top_students(mongo_collection):
    """
    Function returns all students sorted by average score
    """
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])
