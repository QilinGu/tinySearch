#!/usr/bin/python3.2
# Filename Spider.py
# -*-coding:utf-8 -*-


import pymysql

# 数据库操作

# insert into 语句中，单引号换成了双引号，防止music.douban.com/tag/SineadO'Connor这种情况出现
# create database database_name
# 在get_data中，执行后，返回的是数据库游标



class DBProcess(object):

    def __init__(self, user_name, pass_word, db_name, table_name):
        self.conn = pymysql.connect(host='127.0.0.1', user=user_name, passwd=pass_word,db=db_name, port=3306, \
                                    charset='utf8')
        self.cur = self.conn.cursor()
        self.table_name = table_name    # 操作的表的名字

    def get_data(self, command):
        self.cur.execute(command)
        return self.cur

    def insert_data_c(self, url, md5, file_path, file_name):
        try:
            # print("INSERT INTO "+self.table_name+" VALUES(NULL,\'"+url+"\',\'"+md5+"\',\'"+file_path+"\',\'"+file_name+"\')")
            self.cur.execute("INSERT INTO "+self.table_name+" VALUES(NULL,\""+url+"\",\""+md5+"\",\""+file_path+"\",\""+file_name+"\")")
            self.conn.commit()   # 提交
        except pymysql.ProgrammingError as e:
            print("url is: %s md5 is %s  file_path is: %s file_name is: %s" % (url, md5, file_path, file_name))
            exit(-1)

    def insert_data(self, command):
        try:
            print(command)
            self.cur.execute(command)
            self.conn.commit()  # 提交
        except pymysql.err.ProgrammingError as e:
            print(command)
            print(e)

    def close_db(self):
        self.cur.close()
        self.conn.close()

    def fetch_all(self, command):
        self.get_data(command)
        return self.cur.fetchall()


if __name__ == '__main__':
    db = DBProcess('root', '19920102', 'Web', 'PgIndex')
    db.insert_data('NULL', 'NULL', '/home/scottdw/WEB_RAW_FILE/', 'RAW_WEB_2941')
    db.close_db()


