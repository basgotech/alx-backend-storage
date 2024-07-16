#!/usr/bin/env python3
"""
Insert a file in DB using Python
"""


def insert_school(mongo_collection, **kwargs):
    """
     inserts a new DB File
    """
    NEW_DB = mongo_collection.insert_one(kwargs)
    return NEW_DB.inserted_id
