#!/usr/bin/env python3
"""
fetch single row
"""


def schools_by_topic(mongo_collection, topic):
    """
     fetch the list of school having a specific topic

    :param mongo_collection:
    :param topic:
    :return:
    """
    return mongo_collection.find({"topics": topic})
