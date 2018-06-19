import os
import time
from util import HTTP
from util import LXML
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
from model import HDQWallsModel, OriginalFileInfoModel

# 基础网址
base_url = "https://hdqwalls.com"
paging_url = base_url + "/latest-wallpapers/page/"
# mongodb数据库对象
db_client = MongoClient(host="127.0.0.1", port=27017)
db_collection = db_client.python_spider.hdqwalls_spider

# 起始终止位置
START_PAGING_INDEX = 1
END_PAGING_INDEX = 1

# 重试间隔
RETRY_INTERVAL = 2

# 最大并发数
MAX_WORKS = 10


def db_update(model):
    """
    数据库更新，存在则覆盖，不存在则插入
    :param model: 要插入的数据对象
    :return:
    """
    model_dict = {}
    model_dict.update(model.__dict__)
    db_collection.update({"detail_url": model.detail_url}, model_dict, upsert=True)
    print("已插入到数据库：" + model.detail_url)
    pass


def parse_wallpaper_detail(url, title):
    """
    解析壁纸详情页面
    :param url:详情页地址
    :param title:壁纸名称
    :return:
    """
    model = HDQWallsModel.HDQWallsModel(time.time())
    model.update_timestamp = time.time()
    model.detail_url = url
    model.title = title
    # 请求详情页
    selector = LXML.get_selector(HTTP.get(url).content)
    model.author = LXML.get_first_attr_text(selector, "//a[@href and @target and @class]/i", "佚名")
    model.author_link = LXML.get_first_attr(selector, "//a[@href and @target and @class]/i/..", "href", "")
    model.original_resolution = LXML.get_first_attr_text(selector, "//blockquote/footer/a[not(@style)]")
    # 解析分类标签(仅英文)
    categories = []
    for tag in selector.xpath("//div/ul/li[@id='tags']/../a/li/span"):
        categories.append(tag.text.rstrip(",").rstrip("wallpapers").replace("-", " ").strip())
    model.category_list = categories
    # 解析原始文件信息
    original_file = OriginalFileInfoModel.OriginalFileInfoModel()
    original_file.download_url = base_url + LXML.get_first_attr(selector,
                                                                "//div[@class='wallpaper_container']/div/a[@rel='nofollow']",
                                                                "href")
    original_file.file_name = os.path.basename(original_file.download_url)
    original_file.file_format = original_file.file_name[original_file.file_name.index(".") + 1:]
    model.original_file_info.update(original_file.__dict__)
    print("解析完成:", title, url)
    db_update(model)
    print("数据库写入完成")
    pass


def parse_paging(index):
    """
    分页解析，同步方法
    :param index: 页码
    :return:
    """
    if index <= END_PAGING_INDEX:
        response = HTTP.get(paging_url + str(index))
        if response.status_code == 200:
            # 请求成功则解析页面内容
            print("开始解析第", index, "页数据")
            with ThreadPoolExecutor(MAX_WORKS) as executor:
                selector = LXML.get_selector(response.content)
                for tag in selector.xpath("//a[@class='caption hidden-md hidden-sm hidden-xs']"):
                    url = base_url + tag.get("href")
                    title = tag.get("title")
                    executor.submit(parse_wallpaper_detail, url, title)
        elif response.status_code == 403:
            # 如果为403则代表封ip了，需要终止访问
            print("请求第", index, "页出现403，分页终止!")
        else:
            print("请求第", index, "页失败，", RETRY_INTERVAL, "秒后重试")
            time.sleep(RETRY_INTERVAL)
            parse_paging(index)


# 入口
if __name__ == "__main__":
    parse_paging(START_PAGING_INDEX)
    pass
