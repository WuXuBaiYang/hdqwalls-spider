import os
import json
from pymongo import MongoClient

# mongodb数据库对象
db_client = MongoClient(host="127.0.0.1", port=27017)
db_collection = db_client.python_spider.hdqwalls_spider

# 翻译对照表
word_translator_path = os.path.dirname(__file__) + "/WordTranslator.json"


def collection_word():
    """
    整理单词
    :return:
    """
    index = 0
    en_words = {}
    with open(word_translator_path, mode="r", encoding="utf-8") as f:
        file_info = f.read()
        if len(file_info) > 0:
            en_words.update(json.loads(file_info))
    for item_dict in db_collection.find():
        for category in item_dict["category_list"]:
            if category not in en_words:
                en_words.update({category: ""})
        index += 1
        print(index, item_dict["title"])
    print("分类解析完毕，共", len(en_words), "个单词")
    with open(word_translator_path, mode="w", encoding="utf-8") as f:
        f.write(json.dumps(en_words))
    pass


# 入口
if __name__ == "__main__":
    collection_word()
    # item_dict.update(model.__dict__)
    # db_collection.update({"detail_url": model.detail_url}, item_dict, upsert=True)
    pass
