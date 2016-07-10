#!/usr/bin/python3.2
# Filename Spider.py
# -*-coding:utf-8 -*-

import requests
import time
import socket
import os
import re

import threading
from bs4 import BeautifulSoup
from ThreadPool import ThreadPool
from queue import Queue


'''
1.要增加异常处理 (完成)
2.完善过滤词
3.相对网址(完成)
4.禁止访问外站(完成，外部链接仍然有无效的情况)
5.写入数据库挺慢的
6.把异常写入log文件中
7.网页去重(数据库去重方法，redis,hashtable-MD5)
8 请求的状态是403，404，505之类的异常均不爬取
9 在大约38000个页面后,不能爬取了
10 使用线程池
11 不再全站抓取，只抓取豆瓣电影，做一个电影查询
12 增加计数器，如果连续计数超过10次，则退出线程，如果所有线程都推出了，把当前的未访问列表，已访问列表，线程计数值，写到磁盘上。方便下次从短的地方开始下载
'''



# 请求头定制
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:31.0) Gecko/20100101 Firefox/31.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'Connection': 'keep-alive',
           'Referer': '"https://movie.douban.com/"'}
cookies = dict(cookies_are="bid=\"XO95nNSJwPg\"; __utma=30149280.807376841.1451836873.1466133258.1466133701.51;"\
                           "__utmz=30149280.1466133701.51.18.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;"\
                           "gr_user_id=2b21ab7b-fe04-485d-af27-8fd4ba0ba442; ll=\"118318\"; "\
                           "viewed=\"25862578_1270150_4908885_26767504_26134213_6785425_10452969_10600795_10477844_10588787\";"\
                           "ct=y; _pk_id.100001.4cf6=6db700d992a83f79.1464225108.32.1466136979.1466133265.;" \
                           " __utma=223695111.226023932.1464225110.1466133258.1466135310.30; " \
                           "__utmz=223695111.1466135310.30.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/;"\
                           "push_noty_num=0; push_doumail_num=7; __utmv=30149280.5042; _vwo_uuid_v2=8A8D9B0F16B1107879952C89A96F56C2|2ec5bffd5541802381aece361a42659c;"\
                           "ap=1; ps=y; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1466135310%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D;"\
                           "_ga=GA1.2.807376841.1451836873; __utmb=30149280.8.10.1466133701;"\
                           "__utmc=30149280; __utmc=223695111; _pk_ses.100001.4cf6=*; __utmb=223695111.0.10.1466135310")


# url 过滤，包含下列字符的链接不提取 带search?的也不能加入
url_word_filter = ['doubanapp', '.apk', '.iso', 'download', 'market',
                   'login', 'register', 'gov', 'location', 'dongxi', 'fm',
                   'ticket', 'app', 'moment', 'partner', 'jobs', 'cinema',
                   'accounts', 'search', 'reader', 'redir', 'buylinks', 'nowplaying',
                   'standbyme', 'mupload']


root_path = "/home/scottdw/WEB_RAW_FILE/"

forbidden_count = 0;

# 网页搜集器
# Gather的所有方法都变为静态的


class Gather(object):
    def __init__(self):
        pass

    # 下载网页
    @staticmethod
    def download_webpage(url):
        current_thread = threading.current_thread()
        global forbidden_count
        flag = True
        r = ""
        try:
            print("%s begin download %s. " % (current_thread.getName(), url))
            r = requests.get(url, headers=headers, allow_redirects=False)  # 禁止重定向
            if r.status_code == 403:            # 状态码如果不是200 ，当成错误处理
                print("%s , response code is: %d" % (current_thread.getName(), r.status_code))
                forbidden_count += 1
                print("forbidden count is: %d" % forbidden_count)
                flag = False
            elif r.status_code != 200:
                forbidden_count = 0
                print("response code is: %d" % r.status_code)
                flag = False
            else:
                flag = True
                forbidden_count = 0
            print('%s download %s done' % (current_thread.getName(), url))
        except requests.ConnectTimeout as e:    # 链接超时
            flag = False
            print("Error:%s" % e)
        except requests.ConnectionError as e:   # DNS查询失败，拒绝链接
            flag = False
            print("Error:%s" % e)
        except requests.HTTPError as e:         # 无效http响应
            flag = False
            print("Error:%s" % e)
        except requests.TooManyRedirects as e:  # 重定向超过设定的值
            flag = False
            print("Error:%s" % e)
        finally:
            return flag, r                      # 将flag 与r 返回

    # 保存网页
    @staticmethod
    def doc_save(request_result, save_path, count):
        if Gather.out_link(request_result.url):                     # 判断是否是外部的网站，如果是，就不保存该网页
            return False
        try:
            version = 'version:0.1\n'
            url = 'url:'+request_result.url+'\n'
            date = 'date:'+time.strftime('%Y-%m-%d %X', time.localtime())+'\n'
            ip = "213.33.1.147\n"
            html_len = 'doc len:'+str(len(request_result.text))+'\n'
            file_header = version+url+date+ip+html_len
            # 文档存储
            doc = file_header+request_result.text
            path = root_path
            if not os.path.exists(path):  # root path
                os.mkdir(path)
            path = root_path+save_path
            if not os.path.exists(path):
                os.mkdir(path)
            file_name = 'RAW_WEB'+'_'+str(count)
            f = open(path+file_name, 'wt')
            f.write(doc)
            f.flush()
            f.close()
            print('web save successful')
        except TypeError as e:        # 可能出现的异常是r是None类型
            pass
            # print("Error:%s" % e)
        except socket.error as e:     # 一般错误
            pass
            # print("Error:%s" % e)
        except socket.gaierror as e:  # 地址查询错误
            pass
            # print("Error:%s" % e)
        return True

    # 提取网页中的url,并存储url到未访问列表中
    @staticmethod
    def extra_urls(request_result):
        soup = BeautifulSoup(request_result.text)
        new_urls = []
        for link in soup.find_all('a'):
            try:
                r = link['href']
                link_to_append = link.get('href')
                res = Gather.url_filter(request_result.url, link_to_append)         # 需要去除不合法的链接 以及 包含特定关键词的链接
                if res[0]:
                    new_urls.append(res[1])
            except KeyError as e:
                pass
                # print("Error:%s" % e)
        return new_urls

    # 网址过滤，去除下载链接，广告链接
    # 过滤javascript: void 0;
    # 还原相对链接
    @staticmethod
    def url_filter(original_url, link_to_append):
        url = link_to_append
        pos = str(url).find('http')
        if pos != 0:            # pos 不为零，说明没有http,有可能是相对地址
            rr = Gather.relate_url(original_url, url)
            if rr[0]:
                link_to_append = rr[1]
            else:
                return False, link_to_append
        else:
            if Gather.out_link(link_to_append):   # 判断是否是外部地址
                return False, link_to_append

        domain_pos = url.find('//')
        url = url[domain_pos+2:]
        domain_end = url.find("/")
        if domain_end == -1:
            return False, link_to_append
        else:
            domain_name = url[:domain_end]
            domain_name_list = domain_name.split('.')
            if "movie" not in domain_name_list:
                return False, link_to_append
            # 如果是movie,过滤不要的网页
        url_element_list = re.split(r'[/.?=&]', url)                     # 将域名分割成单独的词
        element_section = set(url_element_list) & set(url_word_filter)   # 求交集
        if len(element_section):
            return False,link_to_append
        return True, link_to_append


    # 相对链接的判断
    @staticmethod
    def relate_url(original_url, url):
        pos = url.find('/')
        if pos == 0:
            pos_com = original_url.find('.com')
            if pos_com != -1:
                url = original_url[:pos_com+4]+url
                return True, url
            else:
                return False,url

        pos = url.find('?')
        if pos == 0:
            if original_url[-1] != '/':
                url = original_url+'/'+url
            else:
                url = original_url+url
            return True,url
        return False,url

    # 判断是否是外部的链接
    # 改为限定ip地址
    @staticmethod
    def out_link(url):
        split_pos = url.find(':')
        url = url[split_pos+3:]
        first_pos = url.find('/')
        try:
            domain_name = url[:first_pos]
            domain_name_list = domain_name.split('.')
            if "douban" in domain_name:
                return False
            return True
        except socket.gaierror as e:
            print("wrong url is: %s" % url[:first_pos])
            print(e)
            exit(-1)


# 爬虫类


class Spider(object):

    unvisited_urls = dict()    # 存储未访问列表
    visited_urls = dict()
    task_queue = Queue()       # 任务队列

    def __init__(self, seed):
        self.unvisited_urls = seed
        self.gather = Gather()
        self.url = ''
        self.pool = ThreadPool(self.task_queue, 2)   # 启动4个线程
        self.lock = threading.Lock()                 # 初始化锁

    '''
    start  从未访问url列表中取出一条未访问过的url，与run一起打包放到任务队列中
    '''
    def start(self):
        # 在这里读取配置文件
        for key in self.unvisited_urls:
            self.task_queue.put((self.run, key))
        self.pool.wait_all_complete()
        # 在这里把已完成队列和未完成队列写入文件中。

    def run(self, url, *, save_dir, name):           # 工作线程，下载网页，保存网页，提取新的链接,线程需要提供编号，以便存储(命名参数)
        # time.sleep(5)   # 防止ip被封
        result = self.gather.download_webpage(url)   # 下载网页
        if forbidden_count >= 50:                    # 结束整个程序
            print("exit function")
            return False
        if result[0] and self.gather.doc_save(result[1], save_dir, name):      # 保存网页
            self.visited_urls[url] = True            # 标记为已经访问过的网址
            new_url = self.gather.extra_urls(result[1])       # 提取新的url
            self.lock.acquire()
            for u in new_url:                        # 如果该链接既没有访问过，也不存在于待访问列表中，添加网址,这里在多线程中不安全
                if not self.visited_urls.get(u) and not self.unvisited_urls.get(u):
                    # print("%s add" % u)
                    self.unvisited_urls[u] = True
                    self.task_queue.put((self.run, u))
            print("任务队列大小：%d" % self.task_queue.qsize())
            print("已完成任务量：%d" % len(self.visited_urls))
            self.lock.release()

        self.lock.acquire()
        self.unvisited_urls.pop(url)                  # 在未访问列表中删除该网址
        self.lock.release()  # 释放
        print()
        return True


if __name__ == '__main__':
    urls = {'https://movie.douban.com/': True}
    # urls = ['https://http://www.google.cn/']
    spider = Spider(urls)
    spider.start()
    print('done')
