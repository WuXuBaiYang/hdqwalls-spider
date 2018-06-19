from lxml import html


def get_first_node(node, xpath):
    target_list = node.xpath(xpath)
    if len(target_list) > 0:
        return target_list[0]


def get_first_attr(node, xpath, attr, default_value=""):
    """
    获取属性值，排除空参
    :param node:节点
    :param xpath:xpath语句
    :param attr:属性名
    :param default_value 默认值
    :return:
    """
    target_list = node.xpath(xpath)
    if len(target_list) > 0:
        return target_list[0].get(attr)
    return default_value


def get_first_attr_text(node, xpath, default_value=""):
    """
    获取text属性
    :param node:
    :param xpath:
    :param default_value 默认值
    :return:
    """
    target_list = node.xpath(xpath)
    if len(target_list) > 0:
        return target_list[0].text
    return default_value


def get_first_attr_tail(node, xpath, default_value=""):
    """
    获取tail属性
    :param node:
    :param xpath:
    :param default_value 默认值
    :return:
    """
    target_list = node.xpath(xpath)
    if len(target_list) > 0:
        return target_list[0].tail
    return default_value


def get_selector(response):
    """
    解析http请求结果，使用lxml进行解析
    :param response:
    :return:
    """
    return html.fromstring(response)
