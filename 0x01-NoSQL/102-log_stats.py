#!/usr/bin/env python3
"""
update all log
"""
from pymongo import MongoClient


def log_stats():
    """
    update all log
    """
    user = MongoClient('mongodb://127.0.0.1:27017')
    data_store = user.logs.nginx
    totoal_score = data_store.count_documents({})
    get = data_store.count_documents({"method": "GET"})
    post = data_store.count_documents({"method": "POST"})
    put = data_store.count_documents({"method": "PUT"})
    patch = data_store.count_documents({"method": "PATCH"})
    delete = data_store.count_documents({"method": "DELETE"})
    path = data_store.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{totoal_score} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{path} status check")
    print("IPs:")
    sorted_ips = data_store.aggregate(
        [{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}])
    x = 0
    for b in sorted_ips:
        if x == 10:
            break
        print(f"\t{b.get('_id')}: {b.get('count')}")
        x += 1


if __name__ == "__main__":
    log_stats()
