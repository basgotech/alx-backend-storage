#!/usr/bin/env python3
"""
Update school topics
"""


def update_topics(mongo_collection, name, topics):
    """
    update a row file with para listed

    :param mongo_collection:
    :param name:
    :param topics:
    :return:
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
