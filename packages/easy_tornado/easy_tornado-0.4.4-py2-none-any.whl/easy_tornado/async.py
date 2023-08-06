# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018/11/9 14:11
from threading import Thread


def async_call(fn):
    """
    异步调用 decorator
    :param fn: 函数
    :return 包装函数
    """

    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper
