# !/usr/bin/env python3
# -*- coding:utf-8 -*-

from lxml import etree

# list_url = 'http://quote.eastmoney.com/stocklist.html'
#
# html = get_page(list_url)
# tree = etree.HTML(html)
# ul = tree.xpath('//div[@id="quotesearch"]//a[@target="_blank"]/@href')
# sl = tree.xpath('//div[@id="quotesearch"]//a[@target="_blank"]/text()')
# def get_num(s):
#     return s.split('/')[-1].rstrip('.html')
# ul = list(map(get_num, ul))
# sock_dict = dict(zip(sl, ul))
# with open('sock_dict.json', 'w') as f:
#     json.dump

class PagePaser():
    def __init__(self, html):
        self.tree = etree.HTML(html)

    def get_by_xpath(self, x_path):
        l = self.tree.xpath(x_path)
        return l
