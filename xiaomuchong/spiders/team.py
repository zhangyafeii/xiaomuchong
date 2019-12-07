# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response import Response
from xiaomuchong.items import LwwTeamItem, LwwItemLoader
from xiaomuchong import settings


class TeamSpider(scrapy.Spider):
    name = 'team'
    allowed_domains = ['muchong.com']
    start_urls = ['http://muchong.com/f-189-1', "http://muchong.com/f-233-1", "http://muchong.com/f-291-1",
                  "http://muchong.com/f-272-1", "http://muchong.com/f-452-1"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ 解析板块页面，获得管理团队信息 """
        board = settings.BOARD_MAP[response.url.rsplit('-', maxsplit=1)[0]]
        itemloader = LwwItemLoader(item=LwwTeamItem(), response=response)
        itemloader.add_value("board_id", board[0])
        itemloader.add_value("board_name", board[1])
        itemloader.add_xpath("header_name",
                             "//div[@class='solid forum_info xmc_line_lrb'][1]//div[@class='xmc_fl forum_Team'][1]/dl[1]//a/text()")
        itemloader.add_xpath("header_url",
                             "//div[@class='solid forum_info xmc_line_lrb'][1]//div[@class='xmc_fl forum_Team'][1]/dl[1]//a/@href")
        itemloader.add_xpath("moderator",
                             "//div[@class='solid forum_info xmc_line_lrb'][1]//div[@class='xmc_fl forum_Team'][1]/dl[2]//a/text()")
        itemloader.add_xpath("moderator_url",
                             "//div[@class='solid forum_info xmc_line_lrb'][1]//div[@class='xmc_fl forum_Team'][1]/dl[2]//a/@href")
        if response.xpath('//div[@class="xmc_fr forum_duty"]/strong/text()'):
            itemloader.add_xpath("attendance", '//div[@class="xmc_fr forum_duty"]/strong/text()')
        else:
            itemloader.add_value("attendance", "0")
        team_item = itemloader.load_item()
        yield team_item
