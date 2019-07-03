# -*- coding: utf-8 -*-
import scrapy


class ImoocSpider(scrapy.Spider):
    name = 'imooc'
    allowed_domains = ['https://coding.imooc.com/']
    start_urls = ['http://https://coding.imooc.com//']

    def parse(self, response):
        pass
