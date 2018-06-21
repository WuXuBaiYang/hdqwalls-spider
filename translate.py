import os
import json
import random
import hashlib
import requests
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

# 最大翻译并发数
MAX_TRANSLATE_WORKS = 20
# 最大单词转换并发数
MAX_CONVERT_WORKS = 20
# 有道翻译api
base_translate_api = "https://openapi.youdao.com/api"
secret_key = "0FVkGqas3NXuKv3F9Kx4m7OmvFab1nKg"
app_key = "5e586e6d20cb2649"
fromLang = "EN"
toLang = "zh-CHS"
# 数据库
db_client = MongoClient(host="127.0.0.1", port=27017)
db_collection = db_client.python_spider.hdqwalls_spider
db_translate = db_client.python_spider.hdqwalls_spider_translate
# 翻译对照表路径
word_translator_path = os.path.dirname(__file__) + "/WordTranslator.json"


def translate_word(word):
    """
    单词翻译请求
    :param word:
    :return:
    """
    salt = random.randint(1, 65536)
    sign = app_key + word + str(salt) + secret_key
    sign = hashlib.md5(sign.encode("gbk")).hexdigest()
    translate_url = base_translate_api + '?appKey=' + app_key + '&q=' + word + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    response = requests.get(translate_url)
    if response.status_code == 200:
        response_dict = json.loads(response.content)
        return response_dict["translation"] if response_dict["errorCode"] == "0" else []
    else:
        return []
    pass


def translate_word_write_db(word):
    """
    翻译单词并写入到数据库
    :param word:
    :return:
    """
    print("正在翻译", word, end="...\t")
    translate_values = translate_word(word)
    translate_value = translate_values[0] if len(translate_values) > 0 else ""
    db_translate.update({"word_en": word}, {"word_en": word, "word_cn": translate_value}, upsert=True)
    print(translate_value)
    pass


def convert_word_en(item_dict, convert_map):
    """
    进行单词转换并存入数据库
    :param item_dict:
    :param convert_map:
    :return:
    """
    category_list_cn = []
    for word_en in item_dict["category_list"]:
        category_list_cn.append(convert_map.get(word_en))
    item_dict["category_list_cn"] = category_list_cn
    db_collection.update({"detail_url": item_dict["detail_url"]}, item_dict, upsert=True)
    print("已添加", item_dict["title"], "的中文分类翻译")
    pass


def collection_word():
    """
    整理单词
    :return:
    """
    convert_map = {}
    # 读取关联关系表
    print("加载本地翻译对照表")
    for item_dict in db_translate.find():
        convert_map.update({item_dict["word_en"]: item_dict["word_cn"]})
    # 遍历数据库，找出未记录的词进行缓存
    print("查找未翻译单词")
    for item_dict in db_collection.find({"category_list_cn": {"$size": 0}}):
        for category in item_dict["category_list"]:
            if category not in convert_map:
                convert_map.update({category: ""})
    # 遍历本地对照表进行翻译
    print("开始翻译")
    with ThreadPoolExecutor(MAX_TRANSLATE_WORKS) as executor:
        for key in convert_map.keys():
            executor.submit(translate_word_write_db(key)) if len(convert_map.get(key)) == 0 else ""
        executor.shutdown()
    # 写入数据库中未翻译单词
    print("增加中文翻译")
    with ThreadPoolExecutor(MAX_CONVERT_WORKS) as executor:
        for item_dict in db_collection.find({"category_list_cn": {"$size": 0}}):
            executor.submit(convert_word_en(item_dict, convert_map))
        executor.shutdown()
    print("翻译内容处理完成")
    pass


# 入口
if __name__ == "__main__":
    collection_word()
    pass
