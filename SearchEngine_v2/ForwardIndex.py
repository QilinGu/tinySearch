#!/usr/bin/python3.2
# ForwardIndex.py
# -*-coding:utf-8 -*-


import jieba     # 分词库
from DBProcess import DBProcess
from HtmlParser import HtmlParser


# 该文件对提取出来的文本进行分词，并构建前向索引


class ForwardIndex(object):
    forward_index = dict()

    def __init__(self):
        self.db = DBProcess('root', '19920102', 'Web', 'PgIndex')    # 链接数据库
        self.db2 = DBProcess('root', '19920102', 'Web2', 'HtmlInfo')
        self.db2_table_name = 'HtmlInfo'
        self.data_list = self.db.fetch_all("SELECT * FROM PgIndex")  # 获得所有数据
        jieba.initialize()                                           # 初始化模型

    def create_forward_index(self):
        count = 0
        for i in self.data_list:
            # print("url is: %s" % i[1])
            html2txt = HtmlParser(i[1])              # 取得文件
            txt = html2txt.parser_sub_html()         # 获得解析内容
            # 写入数据库
            self.db2.insert_data("INSERT INTO "+self.db2_table_name+" value(NULL,\""+i[1]+"\",\""+txt[0]+"\",\""+txt[1]
                                 + "\",\""+txt[2]+"\",\""+txt[3]+"\")")
            seg_list = []
            for item in txt:
                if item is None:
                    continue
                seg_list.extend(jieba.lcut_for_search(item))    # 对解析的内容进行分词
            # print(seg_list)
            self.forward_index[i[1]] = seg_list      # 前向索引
            count += 1
            if count == 20000:
                break
        self.db2.close_db()
        self.db.close_db()
        return self.forward_index


if __name__ == '__main__':

    fi = ForwardIndex()
    f = fi.create_forward_index()
    for key, val in f.items():
        print(key,val)

