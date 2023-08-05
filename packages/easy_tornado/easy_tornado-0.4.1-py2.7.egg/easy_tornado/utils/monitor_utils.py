# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018/11/6 14:05
import subprocess

from .file_utils import file_exists
from .file_utils import load_file_contents
from .file_utils import remove_file


def kill_process(pid_file_path):
    if not file_exists(pid_file_path):
        return None
    # 读取PID文件
    pid = load_file_contents(pid_file_path)[0].strip()
    # 杀死该进程
    cmd_stop_mt = 'kill -9 %s' % pid
    cmd_stop_mt_sts = subprocess.call(cmd_stop_mt, shell=True)
    if cmd_stop_mt_sts == 0:
        remove_file(pid_file_path)
        return True
    return False
