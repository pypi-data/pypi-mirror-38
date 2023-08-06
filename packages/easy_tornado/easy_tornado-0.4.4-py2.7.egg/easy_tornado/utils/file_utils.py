# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018年8月23日 14:26:49
import hashlib
import json
import os
import shutil
import subprocess
import tempfile

from decorator import contextmanager

from ..functional import deprecated


def abspath(file_obj):
    """
    获取文件绝对路径, 一般在调用文件传__file__对象
    :param file_obj: 文件对象
    :return: 文件的绝对路径
    """
    return os.path.abspath(file_obj)


def absdir(file_obj):
    """
    获取文件所在目录绝对路径, 一般在调用文件传__file__对象
    :param file_obj: 文件对象
    :return: 文件的所在的目录的绝对路径
    """
    _abspath = abspath(file_obj)
    return os.path.dirname(_abspath)


def dirname(path):
    """
    获取路径父路径
    :param path: 路径
    :return: 父路径
    """
    return os.path.dirname(path)


def file_exists(path):
    """
    判断文件是否存在
    :param path: 文件路径
    :return: 文件存在返回True, 否则返回False
    """
    return os.path.exists(path)


def get_file_size(path):
    """
    获取文件大小
    :param path: 文件路径
    :return: 文件大小
    """
    return os.path.getsize(path)


def get_file_lines(path):
    """
    获取文件行数, 通过Shell命令
    :param path: 文件路径
    :return: 文件行数
    """
    if not file_exists(path):
        return -1
    lines = os.popen(r"wc -l %s | awk '{print $1}'" % path).read()
    return int(lines)


def remove_file(path, ignore_errors=True):
    """
    移除文件(文件及目录)
    :param path: 文件路径
    :param ignore_errors: 是否忽略错误
    :raise 若路径不存在, 则无操作; 若路径既非文件且又非目录则产生ValueError
    """
    if not os.path.exists(path):
        return

    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=ignore_errors)
    else:
        raise ValueError('path should be either a file or directory')


def create_if_not_exists(path):
    """
    如果对应路径不存在的话，则进行创建
    :param path: 文件路径
    :return 若文件已存在且非目录, 抛出ValueError异常
    """
    if os.path.exists(path) and not os.path.isdir(path):
        raise ValueError('path {} exists but is not a directory')

    if not os.path.exists(path):
        os.makedirs(path)


@deprecated(new_fn=create_if_not_exists)
def create_if_not_exist_path(file_path):
    create_if_not_exists(file_path)


def concat_path(base_path, sub_path):
    """
    拼接路径
    :param base_path: 基本路径
    :param sub_path: 子路径
    :return: 拼接后的路径
    """
    return os.path.join(base_path, sub_path)


"""
    拼接路径函数别名
"""
cp = concat_path


@deprecated(new_fn=concat_path)
def format_path(base_path, sub_path):
    return concat_path(base_path, sub_path)


def is_abspath(file_path):
    """
    判断是否为绝对路径
    :param file_path: 文件路径
    :return: 若为绝对路径返回True, 否则返回False
    """
    return file_path is not None and isinstance(file_path, str) and file_path.startswith('/')


def refine_path(base_path, holder, key):
    """
    修正路径(将holder中key对应的值增加base_path)
    :param base_path: 基本路径
    :param holder: 路径容器
    :param key: 路径键或索引
    """
    if isinstance(holder, dict):
        assert key in holder
    elif isinstance(holder, list):
        assert isinstance(key, int) and 0 <= key < len(holder)
    else:
        raise TypeError('holder should be either dict or list, but got {}'.format(type(holder)))

    if not is_abspath(holder[key]):
        holder[key] = cp(base_path, holder[key])


def file_md5sum(file_path):
    """
    计算文件的MD5值
    :param file_path: 文件路径
    :return: 文件MD5
    """
    if not os.path.isfile(file_path):
        return
    ctx = hashlib.md5()
    with open(file_path, 'rb') as fp:
        while True:
            b = fp.read(8096)
            if not b:
                break
            ctx.update(b)
    return ctx.hexdigest()


def file_append(path_append_to, path_append_from):
    """
    将path_append_from的文件内容追加文件到path_append_to中
    :param path_append_to: 待追加内容的文件
    :param path_append_from: 待追加内容所在文件
    :return: 追加结果
    """
    kwargs = {
        'path_append_from': path_append_from,
        'path_append_to': path_append_to
    }
    if not file_exists(path_append_to):
        cmd_create_str = 'cp {path_append_from} {path_append_to}'.format(**kwargs)
        return not subprocess.call(cmd_create_str, shell=True) == 0
    cmd_append_str = 'cat {path_append_from} >> {path_append_to}'.format(**kwargs)
    return subprocess.call(cmd_append_str, shell=True) == 0


@deprecated(new_fn=file_append)
def append_to_file(path_append_to, path_append_from):
    return file_append(path_append_to, path_append_from)


def write_pid(path):
    """
    将pid写入到路径所在文件
    :param path: 路径
    """
    with open(path, 'w') as fp:
        fp.write(str(os.getpid()))


def load_file_contents(path):
    """
    读取文件内容
    :param path: 文件路径
    :return: 若文件不存在返回None, 若可正确读取则返回按行分割的内容列表
    """
    if not file_exists(path):
        return None

    with open(path, 'r') as fp:
        return fp.readlines()


def write_line(wfp, line):
    """
    向文件中写入一行
    :param wfp: 文件写对象
    :param line: 行内容
    """
    if wfp:
        wfp.write(line.strip())
        wfp.write('\n')


def write_file_contents(path, contents):
    """
    写入内容至文件
    :param path: 文件路径
    :param contents: 待写入内容
    """
    with open(path, 'w') as wfp:
        wfp.write(contents)


def write_json_contents(path, data):
    """
    写入JSON内容
    :param path: 文件路径
    :param data: 待写入数据
    """
    json_str = json.dumps(data, ensure_ascii=False).encode('utf-8')
    write_file_contents(path, json_str)


def write_iterable_as_lines(path, iterable_obj, obj2line_func=lambda x: x):
    """
    将可迭代的数据按行的形式写入文件
    :param path: 文件路径
    :param iterable_obj: 可迭代对象
    :param obj2line_func: 将对象映射为行的函数
    """
    with open(path, 'w') as wfp:
        for obj in iterable_obj:
            write_line(wfp, obj2line_func(obj))


@contextmanager
def mkdtemp():
    """
    创建临时路径, 并在退出域时删除该路径
    :return: 临时路径
    """
    path = tempfile.mkdtemp()
    create_if_not_exists(path)
    yield path
    shutil.rmtree(path)
