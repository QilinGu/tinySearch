#!/usr/bin/python3.2
# InvertedIndex.py
# -*-coding:utf-8 -*-

# 建立倒排索引
# 遍历前向索引，构建倒排索引
# 对每一个url的分词，判断倒排索引里是否有该分词，如果没有，则加入到倒排索引中，如果存在，则把url加入到该key值对应的value中
# 需要过滤掉停用词

# 由于建立倒排索引的速度(主要是解析文本的时候)过慢，先尝试把倒排索引写入倒数据库中，然后每次用的时候就从数据库里取，并且，每次退出，应该记录
# 已经建立到那一项的倒排索引了
# select()
import re
from ForwardIndex import ForwardIndex

'''
filter_array = ['http', 'href', 'https', '主演', '导演', '演员', '豆瓣', '表演者', '转让', '展开', 'ISBN', '发行时间',
                '介质', '流派','简介','资料','一样']
'''

def filter_punctuation(word):
    l = re.sub(r'[\(\)\?\s:]', '', word)
    return l

# 建立倒排索引


class InvertedIndex(object):
    inverted_index = dict()

    def __init__(self):
        self.forward = ForwardIndex()
        self.forward_index = self.forward.create_forward_index()

    def create_inverted_index(self):
        for key, value in self.forward_index.items():  # 遍历每一个元素
            for word in value:                         # 对每一个元素，首先判断是否是不检索词，是否是标点符号
                word_after_filter = filter_punctuation(word)
                if len(word_after_filter) <= 1:
                    continue
                print("word:%s will build inverted index len %d" % (word_after_filter, len(word_after_filter)))
                if word_after_filter in self.inverted_index:
                    self.inverted_index[word_after_filter].append(key)
                else:
                    self.inverted_index[word_after_filter] = [key]
        return self.inverted_index


if __name__ == '__main__':
    index = InvertedIndex()
    index.create_inverted_index()

