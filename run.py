# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
from multiprocessing import Process
from page_downloader import get_page, GetHTMLBySele
from page_parser import PagePaser
from storage import DataBase
from IP.IPPool import IPPool
from queue import Queue
from stock_dict import get_stock_dict
import conf

if __name__ == '__main__':
    ip = IPPool()
    q_t = Queue(maxsize=10)  # 任务列队
    q_r = Queue()  # 结果列队
    q_ip = Queue(maxsize=10)

    def ip_put(q_ip):
        while True:
            q_ip.put(ip.get_ip)

    def task_put(q_t):
        for k in get_stock_dict.get():
            q_t.put(k)

    def task_process(q_ip, q_r, q_t):
        proxy = q_ip.get()
        stock_num = q_t.get()
        url = conf.INFO_URL.format(stock_num)
        html = get_page(url, proxy=proxy)
        page = PagePaser(html)
        info = page.get_by_xpath()
        q_r.put(info)
        pass

    def task_process_thread(q_ip, q_r, q_t):
        while True:
            t = Thread(target=task_process, args=(q_ip, q_r, q_t,))
            t.start()

    def store(q_r):
        while True:
            db = DataBase(conf.DATABASE, 'stock')
            info = q_r.get()
            db.store_to_mysql(conf.TABLE_STRUCTOR, info)

    proc_ip = Process(target=ip_put, args=(q_ip,))
    proc_ip.start()
    proc_t = Process(target=task_put, args=(q_t,))
    proc_t.start()
    proc_r = Process(target=task_process_thread, args=(q_ip, q_r, q_t))
    proc_r.start()
    proc_s = Process(target=store, args=(q_r,))
    proc_s.start()
    proc_s.join()
    proc_ip.terminate()
    print('爬取完成！')