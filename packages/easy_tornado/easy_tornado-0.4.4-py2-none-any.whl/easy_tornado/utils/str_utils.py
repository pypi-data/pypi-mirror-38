# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018年8月23日 14:26:49
import hashlib
import json


def md5sum(text):
    """
    获取文本的MD5值
    :param text: 文本内容
    :return: md5摘要值
    """
    _ctx = hashlib.md5()
    _ctx.update(text.encode('utf-8'))
    return _ctx.hexdigest()


def parse_json(json_str):
    """
    将json字符串解析为Python数据
    :param json_str: json字符串
    :return: python对象(dict)
    """
    return json.loads(json_str)
