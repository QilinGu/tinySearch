#!/usr/bin/python3.2
# DBuildInvertedIndex.py
# -*-coding:utf-8 -*-

# 数据库存储倒排索引记录，将倒排索引的建立与查询分离
# 数据库会遇到字符解析的问题，

# -----------------------------------------------------------
# 方法一：
# 创建数据库的时候，url_set 的类型是mediumtext，能存下足够多的url
# 命令:show variables like"character_set_%";
# 默认情况下，character_set_database 的值是：latin1
# 使用命令： set character_set_database = uft8;
# 将字符集更改为utf8
# 重启mysql服务  ubuntu环境下：/etc/init.d/mysql start    /etc/init.d/mysql stop   /etc/init.d/mysql restart
# --------------------------------------------------------------

# xxxx 方法一不起作用  xxxx
# 解决中文存储： 在链接数据库时，指定编码方式为utf-8
# 但是这样并没有根本解决问题，所以需要设置数据库的解析编码格式
# --------------------------------------------------------------------
# 方法二成功:
# 方法一是可行的，需要再重新建立数据库然后插入数据就能成功显示，以前插入的数据一样不会成功显示。
# 命令：alter database xxx CHARACTER SET UTF8 是改变数据库编码格式的

import pymysql
from DBProcess import DBProcess             # 数据库操作
from InvertedIndex import InvertedIndex     # 倒排索引的建立

# 该类的功能，将倒排索引存储到数据库中。

# -----------------------------------------------------------------------
# 网页信息，包含字段： 1.url    2. title.   3.keywords 4.description
#


class DBuildInvertedIndex(object):
    def __init__(self):
        self.table_name = "InvertedIndex"
        self.db = DBProcess('root', '19920102', 'Web2', 'InvertedIndex')   # 链接数据库
        self.inverted_ob = InvertedIndex()
        self.inverted_index = self.inverted_ob.create_inverted_index()     # 创建倒排索引

    def write_index_to_db(self):
        count = 1
        for item in self.inverted_index:
            url_set = "\n".join(self.inverted_index[item][0:])
            print("INSERT INTO " + self.table_name + " VALUE(NULL, \"" + item + "\",\"" + url_set + "\")")
            try:
                self.db.insert_data("INSERT INTO "+self.table_name+" VALUE(NULL ,\""+item+"\",\""+url_set+"\")")
                print("insert success!  %d" % count)
                count += 1
            except pymysql.err.ProgrammingError as e:
                print("INSERT INTO " + self.table_name + " VALUE(NULL, \"" + item + "\",\"" + url_set + "\")")
                print(e)
        self.db.close_db()


if __name__ == "__main__":
    test = DBuildInvertedIndex();
    test.write_index_to_db()

    # db = DBProcess('root', '19920102', 'Web2', 'InvertedIndex')
    # res = db.fetch_all("select * from InvertedIndex")
    # for it in res:
    #    print(it)


