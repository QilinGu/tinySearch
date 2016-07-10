#! /usr/bin/python3
# Filename: GetPage.py
# -*-coding:utf-8 -*-

'''

根据给定的url获得原始网页

'''

# 根据url获取原始网页
import hashlib
from DBProcess import DBProcess


class GetPage(object):
    url = ''
    file_path = ''
    md5 = ''
    file_name = ''

    def __init__(self, url=''):
        self.url = url
        self.file_path = ''
        self.db = DBProcess('root', '19920102', 'Web', 'PgIndex')    # 链接数据库

    def get_content(self):
        self.get_path()                         # 获取文件路径
        full_path = self.file_path+self.file_name
        # print(full_path)
        try:
            with open(full_path, 'rt') as f:         # 读取文件
                file_content_temp = f.readlines()
                file_content = file_content_temp[5:]
            md5_temp = self.md5sum(file_content)
            if md5_temp != self.md5:
                print('md5 is not equal')
        except IOError as e:
            print(full_path)
            print(e)
        return file_content

    def get_path(self):   # 根据指定url获得指定文件的路径
        query_res = self.db.get_data("SELECT MD5,FILE_PATH,FILE_NAME FROM PgIndex WHERE URL="+"\""+self.url+"\"")   # 查询url
        if query_res:
            query_list = []
            for column in query_res:
                query_list = [x for x in column]
            if len(query_list):
                self.md5 = query_list[0]
                self.file_path = query_list[1]
                self.file_name = query_list[2]
            else:
                print('error')
        else:
            print('no such record.')

    def md5sum(self, data):  # 计算文件的MD5值
        if isinstance(data, str):  # 在python 3中，类型unicode改为了str
            data = data.encode("utf-8")
        elif not isinstance(data, str):
            data = str(data).encode("utf-8")
        fd = hashlib.md5()
        fd.update(data)
        return fd.hexdigest()

if __name__ == '__main__':
    get_pg = GetPage('book.douban.com/\n')
    get_pg.get_content()





