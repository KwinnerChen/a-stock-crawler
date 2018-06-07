# !/usr/bin/env python3
# -*- coding:utf-8 -*-

from lxml import etree

class PagePaser():
    def __init__(self, html):
        self.tree = etree.HTML(html)

    def get_by_xpath(self, x_path):
        l = self.tree.xpath(x_path)
        return l
