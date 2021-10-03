# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 16:43:54 2020

Scrapy

@author: rmileng
"""

import scrapy

class MofanSpider(scrapy.Spider):
    name = "mofan"
    start_urls = [
        'https://morvanzhou.github.io/',
    ]
    # unseen = set()
    # seen = set()      # we don't need these two as scrapy will deal with them automatically

    def parse(self, response):
        yield {     # return some results
            'title': response.css('h1::text').extract_first(default='Missing').strip().replace('"', ""),
            'url': response.url,
        }

        urls = response.css('a::attr(href)').re(r'^/.+?/$')     # find all sub urls
        for url in urls:
            yield response.follow(url, callback=self.parse)     # it will filter duplication automatically
# 我们使用 python 的 yield 来返回搜集到的数据 (为什么是yield? 因为在 scrapy 中也有异步处理, 加速整体效率).

# lastly, run this in terminal
# scrapy runspider scrapylys.py -o res2.json (FEED_EXPORT_ENCODING=utf-8) if in chinese