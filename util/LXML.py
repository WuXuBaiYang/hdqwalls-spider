from lxml import html


def get_first_attr(node, xpath, attr):
    """
    获取属性值，排除空参
    :param node:节点
    :param xpath:xpath语句
    :param attr:属性名
    :return:
    """
    target_list = node.xpath(xpath)
    if len(target_list) > 0:
        return target_list[0].get(attr)
    return ""


def get_first_attr_text(node, xpath):
    """
    获取text属性
    :param node:
    :param xpath:
    :return:
    """
    target_list = node.xpath(xpath)
    if len(target_list) > 0:
        return target_list[0].text
    return ""


def get_first_attr_tail(node, xpath):
    """
    获取tail属性
    :param node:
    :param xpath:
    :return:
    """
    target_list = node.xpath(xpath)
    if len(target_list) > 0:
        return target_list[0].tail
    return ""


def get_selector(response):
    """
    解析http请求结果，使用lxml进行解析
    :param response:
    :return:
    """
    return html.fromstring(response)
