# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo
from mysql.connector import Connect

class StorageMethodError(Exception):
    def __str__(self):
        return '存储方法使用错误！'
    __repr__ = __str__

class DataBase():
    '''用于将数据存储到数据库，使用前确保启动了数据库服务，支持MongoDB和MySQL。mongodb使用store_to_mongo()方法，MySQL使用store_to_mysql()方法。
       用于存储的数据须是字典类型。最后可用close()方法关闭数据库。'''
    def __init__(self, dbtype, dbname, host=None, port=None, username=None, password=None):
        self.dbtype = dbtype
        if self.dbtype.lower() == 'mongodb':
            self.username = username
            self.password = password
            self.host = host
            self.port = port
            self.dbname = dbname
            self.db = pymongo.MongoClient(host=self.host, port=self.port, username=self.username, password=self.password)[self.dbname]
            print('连接到数据库%s。' % self.dbname)
        elif self.dbtype.lower() == 'mysql':
            self.dbname = dbname
            self.user = 'root'
            self.password = password
            self.host = 'localhost'
            self.port = 3306
            self.db = self._connect_db()
            print('连接到数据库%s。' % self.dbname)

    def store_to_mongo(self, collection_name, info): # info必须是字典类型
        '''-collection_name: 要存储到的集合，任意字符串。
           -info：要存储的数据，须是字典'''
        if self.dbtype.lower() == 'mongodb':
            id = self.db[collection_name].insert(info)
            print('"%s" 存储到id=%s。' % (tuple(info.values())[0],id))
        else:
            raise StorageMethodError

    def _connect_db(self): # 如果是数据库名链接不上，则创建该名称的数据库，返回的是一个连接实例
        try:
            con = Connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.dbname)
            return con
        except Exception as e:
            if str(e)[:4] == '1049':
                con = Connect(host=self.host, port=self.port, user=self.user, password=self.password)
                cur = con.cursor()
                cur.execute('CREATE DATABASE %s' % self.dbname)
                con = Connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.dbname)
                return con
            else:
                print('MySQL数据库初始化错误，错误信息是：%s' % str(e))

    def _create_table(self, cur, table_structor): # 根据配置文件中的table_structor变量创建数据库表
        txt = 'id int PRIMARY KEY AUTO_INCREMENT NOT NULL, '
        for k,v in tuple(table_structor.values())[0].items():
            txt = txt + k + ' ' + v + ', '
        txt = "CREATE TABLE %s (%s)" % (tuple(table_structor.keys())[0], txt+'时间 timestamp NOT NULL')
        try:
            cur.execute(txt)
        except Exception as e:
            print('创建数据库表时出错：%s。' % e)

    def store_to_mysql(self, table_structor, info): # table_structor是关于数据库结构的一个二维字典，info存储信息，为字典型
        '''-table_structor: 数据库表结构一个二维字典{'table_name':{'title':'varchar(50)', 'summary':'text'}}
           -info: 要存储的数据，须是字典类型'''
        if self.dbtype.lower() == 'mysql':
            txt = ''
            for v in info.values():
                txt = txt + '"%s"'%v + ', '
            txt = "INSERT INTO %s VALUES (Null, %sNull)" % (tuple(table_structor.keys())[0], txt)
            cur = self.db.cursor()
            try:
                cur.execute(txt)
                print('%s存储完成！' % tuple(info.values())[0])
            except Exception as e:
                if str(e)[:4] == '1146':
                    self._create_table(cur, table_structor)
                    cur.execute(txt)
                    print('"%s"存储完成！' % tuple(info.values())[0])
                else:
                    print('存储数据出错，错误信息：%s' % (str(e),))
            finally:
                self.db.commit()
        else:
            raise StorageMethodError

    def close(self):   # 用于关闭数据库连接
        if self.dbtype.lower() == 'mysql':
            self.db.close()
        elif self.dbtype.lower() == 'mongodb':
            self.db.client.close()

if __name__ == '__main__':
    info = {'姓名':"陈", '描述':"好"}
    db = DataBase('mongodb', 'test')
    db.store_to_mongo('test', info)
    db.close()

