from util import HTTP
from model import HDQWallsModel
from pymongo import MongoClient

db_client = MongoClient(host="127.0.0.1", port=27017)
db_collection = db_client.python_spider.hdqwalls_spider


def db_insert(model):
    """
    数据库插入
    :param model: 要插入的数据对象
    :return:
    """
    model_dict = {}
    model_dict.update(model_dict.__dict__)
    db_collection.insert(model_dict)
    print("已插入到数据库：" + model.name)
    pass


# 入口
if __name__ == "__main__":
    pass
