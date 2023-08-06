# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018/11/6 14:05
import signal
from os import kill

from .file_utils import file_exists
from .file_utils import load_file_contents
from .file_utils import remove_file


def kill_process(pid_path, signum=None):
    if not file_exists(pid_path):
        return None

    if signum is None:
        signum = signal.SIGKILL

    # 读取PID文件
    pid = int(load_file_contents(pid_path)[0].strip())

    # 向该进程发送信号
    try:
        kill(pid, signum)
    except OSError as e:
        if len(e.args) != 2 or e.args[1] != 'No such process':
            raise

    # 移除PID文件
    remove_file(pid_path)
