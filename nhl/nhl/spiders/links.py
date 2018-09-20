# -*- coding: utf-8 -*-
import scrapy


class LinksSpider(scrapy.Spider):
    name = 'links'
    allowed_domains = ['www.nhl.com']
    start_urls = ['http://www.nhl.com/']

    def parse(self, response):
        pass
