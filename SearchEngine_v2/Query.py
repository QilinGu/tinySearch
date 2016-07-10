#!/usr/bin/python3.2
# Query.py
# -*-coding:utf-8 -*-

# 查询类，查询的后台服务
import jieba             # 分词类
from InvertedIndex import InvertedIndex
from HtmlParser import HtmlParser
from DBProcess import DBProcess

# 思路：链接倒排索引数据库
#      对查询的词进行分词
#      从数据库中取出结果
#      呈现


# 存在的问题:   1.数据存储方式。现在的方式是将网页数据以单个文本数据存储在磁盘上，然后建立索引的时候，再从磁盘中读取数据，解析。
#                优点：简单方便。 缺点:读取数据速度太慢。
#              2.查询结果不够好。可能的原因在于：1.数据样本小。只有1万份数据，但是却包含了电影，读书，音乐，小组，阅读等全站内容。
#                                           2. 建立索引的关键字的选取
#                                           3. 索引排名

# 要解决的问题： 1.爬虫：改为多线程爬取。  （完成）
#             2.爬取结果的保存方式，方便后续处理(主要是上面第一点的问题)  （已把内容，以及倒排索引存储在数据库中）
#


# 查询结果能呈现，但结果不准确，需要做的工作，pagerank，查询内容与结果的相关度问题


class Query(object):

    def __init__(self):
        self.table_name = "InvertedIndex"
        self.db = DBProcess('root', '19920102', 'Web2', 'InvertedIndex')   # 链接数据库
        self.db_html_info = DBProcess('root', '19920102', 'Web2', 'HtmlInfo')    # 链接网页信息数据库(经过了解析后的网页信息)
        self.html_table_name = 'HtmlInfo'
        self.result = dict()
        self.info_parser = ''

    def get_response(self, query_word):
        cut_word_list = jieba.lcut_for_search(query_word)   # 查询分词
        print("查询分词:")
        print(cut_word_list)
        self.result = dict()
        for word in cut_word_list:
            query_list = self.db.fetch_all("SELECT * FROM "+self.table_name+" WHERE keyword="+"\""+word+"\"")  # 倒排索引数据库
            for item in query_list:
                url_list_temp = item[2]
                url_list = url_list_temp.split('\n')
                for url in url_list:
                    if not self.result.get(url) and url != '':       # 要却掉网页为空的情况，以及去重
                        self.result[url] = True
        print("解析后，对应的网址有:")
        for key in self.result:
            print(key)

    '''
    def show_response(self):
        for item in self.result:
            self.info_parser = HtmlParser(item+'\n')              # 因为存储网址后面有'\n'，所以后面加上'\n'
            title = self.info_parser.title_parser()
            if title:
                print("标题 %s" % title)
            keywords = self.info_parser.keywords_parser()
            if keywords:
                print("关键字 %s" % keywords)
            description = self.info_parser.description_parser()
            if description:
                print("简介：%s " % description)
            if title:
                print("https://%s" % item)
            print()
    '''

    def show_response(self):
        print("查询结果如下：")
        for key in self.result:
            url = key+'\n'
            info = self.db_html_info.get_data("SELECT * FROM "+self.html_table_name+" WHERE url="+"\""+url+"\"")
            show_info = info.fetchall()
            if len(show_info):
                show_url = show_info[0][1]
                title = show_info[0][2]
                keyword = show_info[0][3]
                descr = show_info[0][4]
                brief = show_info[0][5]
                print("url:%s" % show_url)
                print("title: %s" % title)
                print("keyword: %s" % keyword)
                print("descr: %s" % descr)
                print("brief: %s" % brief)
                print('----------------------------')

if __name__ == '__main__':
    q = Query()
    while True:
        words = input()
        q.get_response(words)     # 得到网址集合
        q.show_response()         # 获取网页，并显示结果（获取网页,磁盘上的，然后再解析会比较慢，对当前数据库中的所有网址，解析，把解析结果存储在数据库中）
        print('query done')       # 然后获取结果，直接从数据库中获取
