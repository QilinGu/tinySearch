#! /usr/bin/python3
# Filename: HtmlParser.py
# -*-coding:utf-8 -*-

from bs4 import BeautifulSoup
from GetPage import GetPage


# 思路： 获取一张网页，提取网页title , 提取网页 wrapper->div,subject clearfix  如果查找失败，那么该网页不是介绍单个作品的
# 如果是介绍单个作品的，提取 作品信息，作品简介(其他内容不提取)
# 如果不是单个作品，对于豆瓣小组，成员，小站搜索
# 应该只解析title以及作品出版信息即可，不然分词太多，关联网页太多，而相关网页又太少
# 可以提取<meta>标签里的keywords 以及description内容

# ------------------------------------------------
# 针对豆瓣电影，提取 1.title, 2.keywords 3.description 4.

class HtmlParser(object):
    title = ''
    summary = ''
    brief = ''
    keywords = ''
    description = ''

    def __init__(self, url):
        self.url = url
        self.get_page = GetPage(url)
        self.page_data = self.get_page.get_content()
        self.page_data = "".join(self.page_data[0:])  # 不要直接就用str来转换
        self.soup = BeautifulSoup(self.page_data)

    def title_parser(self):
        try:
            head = self.soup.find("title")  # 网页title
            title_text = head.get_text()
            self.title = self.clean_data(title_text)
        except AttributeError:
            self.title=''
            print("No Title")
        finally:
            return self.title

    def info_parser(self):
        try:
            summ = self.soup.find('div', id="link-report")  # 是对该页作品的简介
            summary_text = summ.get_text()
            self.summary = self.clean_data(summary_text)
        except AttributeError:
            self.summary = ''
            print("No Summary")
        finally:
            return self.summary

    def brief_parser(self):
        try:
            brief_info = self.soup.find('div', "subject clearfix")  # 作品信息，包括名字，作者，ISBN编号等
            brief_text = brief_info.get_text()                      # 如果不包含subject clearfix ，返回的是NoneType
            self.brief = self.clean_data(brief_text)
        except AttributeError:
            self.brief=''
            print("No brief")
        finally:
            return self.brief

    def keywords_parser(self):
        try:
            key_words_tag = self.soup.find('meta', {"name": "keywords"})
            self.keywords = key_words_tag['content']
        except TypeError as e:
            print("keywords_parser error:%s" % e)
            self.keywords = ''
        finally:
            return self.keywords

    def description_parser(self):
        try:
            description_tag = self.soup.find('meta', {"name": "description"})
            self.description = description_tag['content']
        except TypeError as e:
            print("description error: %s" % e)
            self.description = ''
        finally:
            return self.description

    def parser_sub_html(self):  # 只是针对豆瓣音乐，豆瓣读书，豆瓣电影的提取
        self.title_parser()
        self.keywords_parser()
        self.description_parser()
        self.brief_parser()
        # self.info_parser()
        # print("title: %s " % self.title)
        # print("brief: %s" % self.brief)
        # print("summary: %s " % self.summary)
        return self.title, self.keywords, self.description, self.brief   # 先不解析作品简介

    def clean_data(self,data):          # 把数据清理，去除特殊符号
        data = data.replace('\\n', '')  # 去除\n,',,，左右两端空格
        data = data.replace('\\t', '')
        data = data.replace('\\f', '')
        data = data.replace('\\v', '')
        data = data.replace('\\r', '')
        data = data.replace('\'', '')
        data = data.replace(',', '')
        data = data.lstrip().rstrip()
        data = " ".join(data.split())
        return data


if __name__ == '__main__':
    p = HtmlParser('movie.douban.com/subject/6873736/cinema/chengdu/\n')
    p.parser_sub_html()

