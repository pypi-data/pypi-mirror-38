# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018年8月23日 14:26:49
from .logging import it_print


def error_exit(errno, error=None):
    """
    打印消息并退出
    :param errno: 错误码
    :param error: 错误内容
    :return: 
    """
    if error is not None:
        it_print(error)
    exit(errno)
