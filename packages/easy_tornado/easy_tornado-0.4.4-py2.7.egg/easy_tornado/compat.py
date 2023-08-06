# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018/11/14 10:53
import sys

import six

python2 = six.PY2
python3 = six.PY3

if python2:
    C_StandardError = StandardError
    C_MAXINT = sys.maxint

if python3:
    C_StandardError = BaseException
    C_MAXINT = sys.maxsize


def cse_message(e):
    """
    获取异常消息
    :param e: 异常实例
    :return: 异常消息
    """
    assert isinstance(e, C_StandardError)

    if python2:
        return e.message

    if python3:
        if len(e.args) >= 1:
            return e.args[0]
        return ''


def utf8decode(text):
    """
    将text解码为unicode
    :param text: 待解码字符
    :return: 解码后的内容
    """
    if python2:
        return text.decode('utf-8')
    return text


def utf8encode(text):
    """
    将text编码为UTF8
    :param text: 待编码内容
    :return: UTF8编码
    """
    if python2:
        return text.encode('utf-8')
    return text
