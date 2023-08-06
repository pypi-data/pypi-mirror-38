# coding:utf-8
import time


def timestamp_to_string(seconds=None, s='%Y-%m-%d %H:%M:%S'):
    seconds = seconds or time.time()
    return time.strftime(s, time.gmtime(seconds))
