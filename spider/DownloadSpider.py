import os
import oss2
import time
import json
import hashlib
from PIL import Image
from util import HTTP
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

# mongodb数据库对象
db_client = MongoClient(host="127.0.0.1", port=27017)
db_collection = db_client.python_spider.hdqwalls_spider

# 最大并发数
MAX_WORKS = 30
# 重试间隔
RETRY_INTERVAL = 2

# 当前图片缓存目录
photos_cache_path = "/Volumes/移动城堡/original_image"
# oss的accesskey路径
oss_access_key_file = "/Users/jianghan/Documents/WallpaperProject/AccessKey.json"


def get_o_clock_of_today():
    local_time = time.localtime(time.time())
    o_clock = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', local_time), '%Y-%m-%d %H:%M:%S'))
    return int(o_clock)


def upload_file():
    """
    文件上传到oss
    :return:
    """
    with open(oss_access_key_file, "r") as f:
        access_key = json.loads(f.read(), encoding="UTF-8")
    auth = oss2.Auth(access_key["AccessKeyId"], access_key["AccessKeySecret"])
    bucket = oss2.Bucket(auth, access_key["Endpoint"], access_key["Bucket"])
    with ThreadPoolExecutor(MAX_WORKS) as executor:
        for root, dirs, files in os.walk(photos_cache_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.getctime(file_path) > get_o_clock_of_today():
                    executor.submit(bucket.put_object_from_file, "original_image/" + file, file_path)
                    print("正在上传", file)
        executor.shutdown()
        print("文件上传完成")
    pass


def download_file(item_dict):
    """
    文件下载
    :param item_dict:
    :return:
    """
    original_file_info = item_dict["original_file_info"]
    download_url = original_file_info["download_url"]
    response = HTTP.get(download_url, use_proxy=True)
    if response.status_code == 200:
        file_format = original_file_info["file_format"]
        file_name = hashlib.md5(download_url.encode("gbk")).hexdigest()
        file_path = photos_cache_path + "/" + file_name + "." + file_format
        with open(file_path, "wb") as f:
            f.write(response.content)
        # 读取文件信息
        Image.MAX_IMAGE_PIXELS = 1000000000
        image = Image.open(file_path)
        original_file_info["width"] = image.width
        original_file_info["height"] = image.height
        original_file_info["file_size"] = os.path.getsize(file_path)
        # 信息赋值并写入数据库
        item_dict["original_file_info"] = original_file_info
        db_collection.update({"detail_url": item_dict["detail_url"]}, item_dict, upsert=True)
        print("图片下载完成", download_url)
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
        executor.shutdown()
        print("文件下载完成")
    pass


# 入口
if __name__ == "__main__":
    handle_db_collection()
    upload_file()
    pass
