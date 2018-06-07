# !/usr/bin/env python3
# -*- coding: utf-8 -*-

'''模块用于获取股票的名称和代码列表，已字典形式存储在json文件中，存在直接读取，不存在则从网络获取。'''

from page_downloader import get_page
from page_parser import PagePaser
import os, json

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stock_dict.json')

def _read_json():
    with open(file_path, 'r') as f:
        stock_l = json.load(f)
        return stock_l

def get():
    if os.path.exists(file_path) and os.path.getsize(file_path)>0:
        print('加载股票列表......')
        l = _read_json()
        return l
    else:
        _refresh()
        print('加载股票列表......')
        l = _read_json()
        return l

def _refresh():
    html = get_page('http://quote.eastmoney.com/stocklist.html')
    if html:
        html_p = PagePaser(html)
        stock_name = html_p.get_by_xpath('//div[@id="quotesearch"]//a[@target="_blank"]/text()')
        stock_num = html_p.get_by_xpath('//div[@id="quotesearch"]//a[@target="_blank"]/@href')
        stock_num = list(map(lambda x: x.split('/')[-1].strip('.html'), stock_num))
        stock_dic = dict(zip(stock_name, stock_num))
        with open(file_path, 'w') as f:
            json.dump(stock_dic, f)

    else:
        raise DownloadErro('http://quote.eastmoney.com/stocklist.html')

class DownloadErro(Exception):
    def __init(self, info):
        self.info = info

    def __str__(self):
        return ' 下载出错：%s' % self.info

    __repr__ = __str__

if __name__ == '__main__':
    dic = get()
    print(len(dic))
