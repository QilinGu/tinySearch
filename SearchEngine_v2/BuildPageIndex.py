#!/usr/bin/python3.2
# Filename Spider.py
# -*-coding:utf-8 -*-

import sys
import hashlib                  # 使用md5
import os

from DBProcess import DBProcess


# 建立网页的索引，更方便的记录网页存储的位置
# 该类包含的数据成员有:pg_index url  MD5  file_path  file_name
# 和数据库里的内容一致

root_path = '/home/scottdw/WEB_RAW_FILE/'


class BuildPageIndex(object):
    url = ''
    MD5 = ''
    head = ''
    file_list = []
    file_dict = []
    file_path = ''
    file_name = ''
    data = ''

    def __init__(self):
        self.db = DBProcess('root', '19920102', 'Web', 'PgIndex') # 链接到数据库
        self.file_path = root_path+''

    def get_dict(self):            # 用于获得指定目录下的子目录 ，没有子目录时返回为空
        dict_temp = os.listdir(root_path)
        self.file_dict = [x for x in dict_temp if os.path.isdir(root_path+x)]

    def get_file(self):          # 用于获取文件列表
        file_temp = os.listdir(self.file_path)
        self.file_list = [x for x in file_temp if os.path.isfile(self.file_path+x)]

    def md5sum(self, data):        # 计算文件的MD5值file_path
        if isinstance(data, str):  # 在python 3中，类型unicode改为了str
            data = data.encode("utf-8")
        elif not isinstance(data, str):
            data = str(data).encode("utf-8")
        fd = hashlib.md5()
        fd.update(data)
        return fd.hexdigest()

    def create_index_dispatch(self, file_path, file_name):
        with open(file_path+file_name, 'rt') as f:
            file_data_temp = f.readlines()
            self.head = file_data_temp[:5]     # 读取头部
            print(self.head[1])                # 打印url
            self.data = file_data_temp[5:]     # 读取数据部分

        self.url = self.head[1]                # 读取url
        self.MD5 = self.md5sum(self.data)      # 计算文件MD5值
        self.file_path = file_path
        self.file_name = file_name
        # 写入到数据库中
        self.url.rstrip()                     # 去除右边的空格
        self.db.insert_data_c(self.url, self.MD5, self.file_path, self.file_name)
        # print("url: %s  MD5: %s file_dict: %s file_name: %s" % (self.url,self.MD5,self.file_path,self.file_name))

    def create_index(self):
        self.get_dict()                                  # 获得文件目录
        if len(self.file_dict):                          # 遍历每一个文件夹
            for dict_temp in self.file_dict:
                self.file_path = root_path+dict_temp+'/'
                self.get_file()                          # 获得当前路径下的所有文件
                for pg in self.file_list:                # 为每一个文件创建数据库元素
                    self.create_index_dispatch(self.file_path, pg)
        else:                                            # 该目录下没有文件夹
            self.file_path = root_path
            self.get_file()
            for pg in self.file_list:
                self.create_index_dispatch(self.file_path, pg)
        self.db.close_db()                                # 存储完毕，关闭数据库


# 创建网页索引


if __name__ == '__main__':
    bd = BuildPageIndex()
    bd.create_index()
    print('done')








