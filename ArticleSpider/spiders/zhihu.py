# -*- coding: utf-8 -*-
import scrapy


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['wwww.zhihu.com']
    start_urls = ['http://wwww.zhihu.com/']

    def parse(self, response):
        pass
