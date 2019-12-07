# -*- coding: utf-8 -*-
import pandas as pd
import scrapy

from xiaomuchong.DBHelper import db_conn
from xiaomuchong.items import LwwItemLoader,LwwUserItem
import itertools


class UsersSpider(scrapy.Spider):
    name = 'users'
    allowed_domains = ['muchong.com']
    # start_urls = ['http://muchong.com/bbs/space.php?uid=1122189']

    @staticmethod
    def get_start_urls():
        team_data = pd.read_sql(sql="select header_url,moderator_url from team", con=db_conn)
        header_urls = [url for header_urls in team_data["header_url"].str.split('\|\|') for url in header_urls]
        moderator_urls = [url for moderator_urls in team_data["moderator_url"].str.split('\|\|') for url in moderator_urls]
        charmer_data = pd.read_sql(sql="select charmer_url from charmer", con=db_conn)
        comments_data = pd.read_sql(sql="select author_url from comment", con=db_conn)
        return header_urls, moderator_urls, charmer_data['charmer_url'], comments_data['author_url']

    def start_requests(self):
        # url需要从数据库中提取
        header_urls, moderator_urls, charmer_urls, author_urls = self.get_start_urls()
        for url in itertools.chain(header_urls, moderator_urls, charmer_urls, author_urls,):
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ 用户表 """
        item_loader = LwwItemLoader(item=LwwUserItem(), response=response)
        item_loader.add_value("user_url", response.url)
        item_loader.add_xpath("user_name", '//div[@class="space_index "]//tr/td[2]/div[1]/a[1]/text()')
        item_loader.add_xpath("listener", 'string(//div[@class="space_index "]//tr/td[2]/div[not(@class or @style)])')
        item_loader.add_xpath("red_flower", 'string(//div[@class="space_index "]//tr/td[2]/div[not(@class or @style)])')
        item_loader.add_xpath("register_time", '//div[@class="user_index_info"]/table[1]//tr/td[1]/text()')
        item_loader.add_xpath("last_active_time", '//div[@class="user_index_info"]/table[1]//tr/td[2]/text()')
        item_loader.add_xpath("last_post_time", '//div[@class="user_index_info"]/table[1]//tr/td[3]/text()')
        item_loader.add_xpath("serial_num", '//div[@class="user_index_info"]/table[2]//tr[1]/td[1]/text()')
        item_loader.add_xpath("user_group", '//div[@class="user_index_info"]/table[2]//tr[1]/td[2]/text()')
        item_loader.add_xpath("help", '//div[@class="user_index_info"]/table[2]//tr[1]/td[3]/text()')
        item_loader.add_xpath("vip", '//div[@class="user_index_info"]/table[2]//tr[2]/td[1]/text()')
        item_loader.add_xpath("gold", '//div[@class="user_index_info"]/table[2]//tr[2]/td[2]/text()')
        item_loader.add_xpath("spend", '//div[@class="user_index_info"]/table[2]//tr[2]/td[3]/text()')
        item_loader.add_xpath("soft", '//div[@class="user_index_info"]/table[2]//tr[3]/td[1]/text()')
        item_loader.add_xpath("posts", '//div[@class="user_index_info"]/table[2]//tr[3]/td[2]/text()')
        if response.xpath('string(//div[@class="user_index_info"]/table[2]//tr[3]/td[3])').extract_first().strip():
            item_loader.add_xpath("rule", 'string(//div[@class="user_index_info"]/table[2]//tr[3]/td[3])')
        else:
            item_loader.add_value("rule", '无')
        item_loader.add_xpath("online", '//div[@class="user_index_info"]/table[2]//tr[4]/td[1]/text()')
        item_loader.add_xpath("online_status", 'string(//div[@class="user_index_info"]/table[2]//tr[4]/td[2])')
        if response.xpath('//div[@class="user_index_info"]/table[2]//tr[4]/td[3]/text()').extract_first().strip():
            item_loader.add_xpath("major", '//div[@class="user_index_info"]/table[2]//tr[4]/td[3]/text()')
        else:
            item_loader.add_xpath("major", '未知')
        item_loader.add_xpath("gender", 'string(//div[@class="user_index_info"]/table[2]//tr[5]/td[1])')
        if response.xpath('//div[@class="user_index_info"]/table[2]//tr[5]/td[2]/text()'):
            item_loader.add_xpath("region", '//div[@class="user_index_info"]/table[2]//tr[5]/td[2]/text()')
        else:
            item_loader.add_value("region", '未知')
        item_loader.add_xpath("birthday", '//div[@class="user_index_info"]/table[2]//tr[5]/td[3]/text()')
        user_item = item_loader.load_item()
        yield user_item