import os
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

# mongodb数据库对象
db_client = MongoClient(host="127.0.0.1", port=27017)
db_collection = db_client.python_spider.hdqwalls_spider

# 最大并发数
MAX_WORKS = 18


def download_file(url):
    """
    文件下载
    :param url:
    :return:
    """
    pass


def handle_db_collection():
    """
    处理数据库中的数据
    :return:
    """
    pass


# 入口
if __name__ == "__main__":
    handle_db_collection()
    pass
