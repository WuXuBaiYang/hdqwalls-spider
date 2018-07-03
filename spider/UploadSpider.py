import os
import json
import time
import oss2
import requests
from model import BatchRequest
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

# 数据库
db_client = MongoClient(host="127.0.0.1", port=27017)
db_collection = db_client.python_spider.hdqwalls_spider

# 最大并发数
MAX_WORKS = 20
START_PAGE = 0
MAX_BATCH = 50

base_url = "https://api.bmob.cn/1/batch"
headers = {"X-Bmob-Application-Id": "390b6a10efdb099c82520d7478ce4bab",
           "X-Bmob-REST-API-Key": "4b26a2e1112982c8f7bbd35168b9c72a",
           "Content-Type": "application/json"}
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


def page_upload(page, limit):
    request_list = []
    for item_dict in db_collection.find({'create_timestamp': {'$gt': get_o_clock_of_today()}}).skip(page * limit).limit(
            limit):
        item_dict.pop("_id")
        item_dict.pop("create_timestamp")
        item_dict.pop("update_timestamp")
        request = BatchRequest.BatchRequest()
        request.body = item_dict
        request.method = "POST"
        request.path = "/1/classes/hdqwalls"
        request_dict = {}
        request_dict.update(request.__dict__)
        request_list.append(request_dict)
    if len(request_list) > 0:
        batch_request = {"requests": request_list}
        response = requests.post(base_url, data=json.dumps(batch_request), headers=headers)
        if response.status_code == 200:
            print("第", page, "页上传完成,共", len(request_list), "条数据")
            page += 1
        else:
            print("上传失败，正在重试", response.status_code)
        page_upload(page, limit)
    else:
        print("所有数据上传完成！")
    pass


# 入口
if __name__ == "__main__":
    page_upload(0, 50)
    upload_file()
    pass
