# -*- coding: utf-8 -*-
import scrapy
from lww.items import LwwItemLoader, LwwCommentItem
from lww.DBHelper import db_conn
import pandas as pd


class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['muchong.com']
    # start_urls = ['http://muchong.com/t-13667321-1']

    @staticmethod
    def get_start_urls(self):
        data = pd.read_sql(sql="posts", con=db_conn, columns=["post_url"])
        return data['post_url']

    def start_requests(self):
        # url需要从数据库中提取
        for url in self.get_start_urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ 评论表 """
        request_url = response.url[:-1]
        comment_nums = response.xpath('//div[@class="xmc_fr xmc_Pages"]//td[1]/text()')[0].extract()
        page_num = int(comment_nums) // 100 + 1
        if page_num > 1:
            for page in range(1, int(page_num) + 1):
                yield scrapy.Request(url=f'{request_url}{page}', callback=self.parse_detail)
        else:
            yield scrapy.Request(url=response.url, callback=self.parse_detail)

    def parse_detail(self, response):
        tbodys = response.xpath('//tbody[starts-with(@id, "pid")]')
        for n, tbody in enumerate(tbodys, start=1):
            item_loader = LwwItemLoader(item=LwwCommentItem(), selector=tbody)
            item_loader.add_value("post_url", response.url)
            item_loader.add_xpath("floor", 'tr/td[@class="pls_foot"]/div/span/a/text()')
            item_loader.add_xpath("author_name", 'string(tr/td[1]/div[contains(@id, "_avatar")]/h3/a)')
            item_loader.add_xpath("author_url", 'tr/td[1]/div[starts-with(@id, "_avatar")]/h3/a/@href')
            item_loader.add_xpath("post_time", 'string(//em[@class="xmc_c9"])')
            if tbody.xpath("tr[1]//td/fieldset"):
                item_loader.add_xpath("reference", "tr[1]//td/fieldset/div/b/u/a/text()")
            else:
                item_loader.add_value("reference", "无")
            item_loader.add_xpath("content", 'string(tr[1]/td[2]/div/div[@class="t_fsz"]/table//tr/td)')
            if tbody.xpath(f'//*[@id="qtop_{n}_{n}"]/a'):
                item_loader.add_xpath("praise_num", f'string(//*[@id="qtop_{n}_{n}"]/a)')
            else:
                item_loader.add_value("praise_num", 0)
            if tbody.xpath('tr/td[@class="pls_foot"]/div/span/a/text()') == "1":
                item_loader.add_value("isTopic", 1)
            else:
                item_loader.add_value("isTopic", 0)
            comment_item = item_loader.load_item()
            yield comment_item