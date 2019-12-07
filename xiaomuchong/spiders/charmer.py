# -*- coding: utf-8 -*-
import scrapy

from xiaomuchong import settings
from xiaomuchong.items import LwwItemLoader,LwwCharmerItem


class CharmerSpider(scrapy.Spider):
    name = 'charmer'
    allowed_domains = ['muchong.com']
    # start_urls = ['http://muchong.com/f-189-1', "http://muchong.com/f-233-1", "http://muchong.com/f-291-1",
    #               "http://muchong.com/f-272-1", "http://muchong.com/f-452-1"]
    start_urls = ['http://muchong.com/f-272-1']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ 解析板块牛人榜成员 """
        board = settings.BOARD_MAP[response.url.rsplit('-', maxsplit=1)[0]]
        li_list = response.xpath('//div[@class="user_Rank bg_global  bg_global_padding"]/ul/li')
        for li in li_list:
            itemloader = LwwItemLoader(item=LwwCharmerItem(), selector=li)
            itemloader.add_value("board_id", board[0])
            itemloader.add_value("board_name", board[1])
            itemloader.add_css("charmer_name", "span a::text")
            itemloader.add_css("charmer_url", "span a::attr(href)")
            itemloader.add_css("effect_index", "em::text")
            charmer_item = itemloader.load_item()
            yield charmer_item
