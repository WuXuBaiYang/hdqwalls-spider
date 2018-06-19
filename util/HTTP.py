import os
import time
import json
import requests
from random import choice

# user_agent列表
user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"
]
# 代理列表
https_proxies_list = []

# 代理服务器列表缓存文件路径
proxies_file_path = os.path.abspath('.') + "/proxies.json"
proxies_refresh_time = 5 * 60

# 代理提取地址
proxies_url = "http://webapi.http.zhimacangku.com/getip?num=20&type=2&pro=&city=0&yys=0&port=11&pack=23142&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions="


def get_headers():
    """
    获取头部参数
    :return: 返回头部参数
    """
    return {
        "User-Agent": choice(user_agent_list)}


def get_proxies():
    """
    获取代理
    :return: 获取代理参数
    """
    # 如果文件不存在或者文件的修改时间与当前时间相差刷新时间，则重新请求并读取文件
    if not os.path.exists(proxies_file_path) or time.time() - os.path.getmtime(
            proxies_file_path) >= proxies_refresh_time:
        # 提取代理ip
        content = requests.get(proxies_url).content
        with open(proxies_file_path, "w") as file:
            file.write(content.decode())
        # 读取json到内存
        read_proxies_from_json(content)
        pass
    elif len(https_proxies_list) == 0:
        # 如果https的缓存列表为空，则从文件中读取
        with open(proxies_file_path, "r") as file:
            read_proxies_from_json(file.read())
        pass
    return {"https": https_proxies_list[0]}


def get(request_url):
    """
    发起http/https get请求 proxies=get_proxies(),
    :param request_url: 请求地址
    :return: 返回request的请求对象
    """
    return requests.get(request_url, headers=get_headers())


def read_proxies_from_json(json_string):
    """
    从json中读取代理ip缓存到内存
    :param json_string:
    :return:
    """
    proxies_json = json.loads(json_string)
    if proxies_json.get("success"):
        ip_address_list = proxies_json.get("data")
        for ip_address in ip_address_list:
            ip = ip_address.get("ip")
            port = ip_address.get("port")
            https_proxies_list.append("https://" + ip + ":" + str(port))
    pass
