#!/usr/bin/python3
# Test.py
# -*- coding:utf-8 -*-

import requests
import time
import socket
import os
import re
import socket
from BuildPageIndex import BuildPageIndex



# 多线程测试
# 线程池的结构：
# 1.线程池管理器，负责线程池的启动，停用，管理
# 2.工作线程，工作中的线程
# 3.请求接口，创建请求对象，供工作线程调用
# 4,请求队列，用于存放和提取对象
# 5.结果队列，用于存放请求执行完毕后的结果

'''
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:31.0) Gecko/20100101 Firefox/31.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'Connection': 'keep-alive'}
host = "https://movie.douban.com/"

try:
    r = requests.get(host, headers=headers, allow_redirects=False)  # 禁止重定向
    print(socket.gethostbyname("movie.douban.com"))
    if r.status_code != 200:
        print("error")
    print(r.status_code)
except requests.HTTPError as e:
    print(e)
'''


def test_fun():
    return 1,None,3

tt = test_fun()
print(tt[0])


