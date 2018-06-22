import os
import time
import hashlib
from PIL import Image
from util import HTTP
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

# mongodb数据库对象
db_client = MongoClient(host="127.0.0.1", port=27017)
db_collection = db_client.python_spider.hdqwalls_spider

# 最大并发数
MAX_WORKS = 20
# 重试间隔
RETRY_INTERVAL = 2

# 当前图片缓存目录
photos_cache_path = os.path.dirname(__file__) + "/photos_cache"


def download_file(item_dict):
    """
    文件下载
    :param item_dict:
    :return:
    """
    original_file_info = item_dict["original_file_info"]
    download_url = original_file_info["download_url"]
    print("正在下载图片", download_url)
    response = HTTP.get(download_url)
    if response.status_code == 200:
        file_format = original_file_info["file_format"]
        file_name = hashlib.md5(download_url.encode("gbk")).hexdigest()
        file_path = photos_cache_path + "/" + file_name + "." + file_format
        with open(file_path, "wb") as f:
            f.write(response.content)
        # 读取文件信息
        image = Image.open(file_path)
        original_file_info["width"] = image.width
        original_file_info["height"] = image.height
        original_file_info["file_size"] = os.path.getsize(file_path)
        # 信息赋值并写入数据库
        item_dict["original_file_info"] = original_file_info
        db_collection.update({"detail_url": item_dict["detail_url"]}, item_dict, upsert=True)
    elif response.status_code == 401:
        print("ip已被封禁，下载停止")
    else:
        print("下载失败", RETRY_INTERVAL, "秒后重试")
        time.sleep(RETRY_INTERVAL)
        download_url(item_dict)
    pass


def handle_db_collection():
    """
    处理数据库中的数据
    :return:
    """
    with ThreadPoolExecutor(MAX_WORKS) as executor:
        for item_dict in db_collection.find({'original_file_info.file_size': 0}):
            executor.submit(download_file, item_dict)
    pass


# 入口
if __name__ == "__main__":
    handle_db_collection()
    pass
