import json
import time
import requests
from model import BatchRequest
from pymongo import MongoClient

# 数据库
db_client = MongoClient(host="127.0.0.1", port=27017)
db_collection = db_client.python_spider.hdqwalls_spider

# 最大并发数
MAX_WORKS = 20

base_url = "https://api.bmob.cn/1/batch"
headers = {"X-Bmob-Application-Id": "390b6a10efdb099c82520d7478ce4bab",
           "X-Bmob-REST-API-Key": "4b26a2e1112982c8f7bbd35168b9c72a",
           "Content-Type": "application/json"}


def get_o_clock_of_today():
    local_time = time.localtime(time.time())
    o_clock = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', local_time), '%Y-%m-%d %H:%M:%S'))
    return int(o_clock)


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
    pass
