from util import HTTP
from util import LXML
import requests
from model import HDQWallsModel
from pymongo import MongoClient

# 基础网址
base_url = "https://hdqwalls.com/latest-wallpapers/page/"
# mongodb数据库对象
db_client = MongoClient(host="127.0.0.1", port=27017)
db_collection = db_client.python_spider.hdqwalls_spider


def db_update(model):
    """
    数据库更新，存在则覆盖，不存在则插入
    :param model: 要插入的数据对象
    :return:
    """
    model_dict = {}
    model_dict.update(model_dict.__dict__)
    db_collection.update({"name": model.detail_url}, model_dict, upsert=True)
    print("已插入到数据库：" + model.detail_url)
    pass


# 入口
if __name__ == "__main__":
    pass
