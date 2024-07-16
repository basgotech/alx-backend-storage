#!/usr/bin/env python3
"""
List all documents DB
"""


def list_all(mongo_collection):
    """
    lists all DB File in a collection
    """
    return mongo_collection.find()
