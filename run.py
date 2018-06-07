# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
from threading import Thread
from multiprocessing import Process, Queue
from page_downloader import get_page
from page_parser import PagePaser
from storage import DataBase
from IP.IPPool import IPPool
from stock_dict import get_stock_dict
import conf


def ip_put(ippool, q_ip):  # 在ip队列中循环放入代理ip
    while True:
        ip = ippool.get_ip
        if ip:
            q_ip.put(ip)

def task_put(stock_dict, q_t):  # 提取股票名和代码，以元组的方式放入任务列队
    while True:
        q_t.put(stock_dict.popitem())

def task_process(url, proxy, stock_name, q_r):  # 任务处理函数，使用代理IP，接受任务列队，结果以字典形式存入结果列队
    stock_dic = dict()
    html = get_page(url, proxy=proxy)
    try:
        page = PagePaser(html)
        stock_dic['股票名称'] = stock_name
        colum = page.get_by_xpath('//div[@class="bets-content"]//dt/text()')
        colum = map(lambda x: x.strip(), colum)  # 去除多余空白
        num = page.get_by_xpath('//div[@class="bets-content"]//dd/text()')
        num = map(lambda x: x.strip(), num)
        stock_dic.update(dict(zip(colum, num)))
        # print(stock_dic)
        q_r.put(stock_dic)
        print('%s %s提取完成。' % (threading.current_thread().name,stock_name))
    except ValueError:
        print('没有%s股票信息。' % stock_name )

def task_process_thread(url_base, task_process, q_ip, q_r, q_t): # 将任务处理函数分派多线程
    while True:
        stock_tup = q_t.get()
        url = url_base.format(stock_tup[1])
        proxy = q_ip.get()
        stock_name = stock_tup[0]
        t = Thread(target=task_process, args=(url, proxy, stock_name, q_r,))
        t.start()

def store(db, db_structor, q_r):
    while True:
        try:
            info = q_r.get(timeout=20)
            if db.dbtype == 'mysql':
                print('%s正在存入数据库。' % info['股票名称'])
                db.store_to_mysql(db_structor, info)
            if db.dbtype == 'mongodb':
                print('%s正在存入数据库。' % info['股票名称'])
                db.store_to_mongo(db_structor, info)
        except:
            return

if __name__ == '__main__':
    q_ip = Queue(maxsize=50) # 代理ip队列
    q_t = Queue(maxsize=15) # 任务队列
    q_r = Queue() # 结果队列
    ippool = IPPool()
    proc_ip = Process(target=ip_put, args=(ippool, q_ip,))
    proc_ip.start()
    stock_dict = get_stock_dict.get()
    proc_t = Process(target=task_put, args=(stock_dict, q_t,))
    proc_t.start()
    url_base = conf.INFO_URL
    proc_r = Process(target=task_process_thread, args=(url_base, task_process, q_ip, q_r, q_t))
    proc_r.start()
    dbtype = conf.DATABASE.get('dbtype')
    dbname = conf.DATABASE.get('dbname')
    password = conf.DATABASE.get('password')
    db = DataBase(dbtype=dbtype, dbname=dbname, password=password)
    proc_s = Process(target=store, args=(db, conf.TABLE_STRUCTOR, q_r,))
    proc_s.start()
    proc_s.join()
    proc_ip.terminate()
    proc_t.terminate()
    proc_r.terminate()
    if not q_t.empty():
        print('任务没有爬取完全！')
    if not q_r.empty():
        print('任务没有存储完全！')
    db.close()
    print('爬取完成！')