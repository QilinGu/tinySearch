#!/usr/bin/python3
# ThreadPool.py
# -*- coding:utf-8 -*-

import threading
import time
from queue import Queue


# 多线程测试
# 线程池的结构：
# 1.线程池管理器，负责线程池的启动，停用，管理
# 2.工作线程，工作中的线程
# 3.请求接口，创建请求对象，供工作线程调用
# 4,请求队列，用于存放和提取对象
# 5.结果队列，用于存放请求执行完毕后的结果

__all__ = ['ThreadPool', 'WorkThread']


class ThreadPool(object):
    def __init__(self, request_queue, thread_num=2):   # 线程池接口，必须提供任务队列，线程数量可选
        self.task_queue = request_queue
        self.threads = []               # 线程队列
        self.__init_thread_pool(thread_num)    # 线程池初始化

    """
        初始化线程
    """
    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            t = WorkThread(self.task_queue)
            self.threads.append(t)

    """
        等待所有线程运行完毕
    """
    def wait_all_complete(self):
        for item in self.threads:
            if item.isAlive():
                print("%s join." % item.getName())
                item.join()
                print("%s terminal." % item.getName())


class WorkThread(threading.Thread):    # 工作线程
    def __init__(self, task_queue):
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.setDaemon(True)
        self.start()

    def run(self):
        # 死循环，从而让创建的线程在一定条件下关闭退出
        count = 0
        save_name = ""
        run_flag = True
        while True and run_flag:
            print("线程 %s 正在运行... count is: %d" % (self.getName(), count))
            do, args = self.task_queue.get()                # 任务异步出队，Queue内部实现了同步机制 get获取一个元素，并从队列中删除# 要设置一个超时值
            print("线程 %s 获得了任务..." % self.getName())
            save_dir = self.getName()+"/"
            save_name = count
            run_flag = do(args, save_dir=save_dir, name=save_name)     # 保存文档
            self.task_queue.task_done()                     # 通知系统任务完成
            time.sleep(5)
            count += 1
            if self.task_queue.empty():
                print("task queue is empty.break")
                break
        # 在这里把计数值写入到文件中
'''
# 具体要做的任务
# 工作函数
def do_job(args):
    print(args)
'''
if __name__ == '__main__':
    start = time.time()
    url_queue = Queue()

    work_manager = ThreadPool(10, 2)#或者work_manager =  WorkManager(10000, 20)
    work_manager.wait_allcomplete()
    end = time.time()
    # print "cost all time: %s" % (end-start)
