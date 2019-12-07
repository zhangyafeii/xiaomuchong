# -*- coding: utf-8 -*-
import scrapy
from xiaomuchong.items import LwwItemLoader,LwwPostItem
from xiaomuchong import settings


class PostsSpider(scrapy.Spider):
    name = 'posts'
    allowed_domains = ['muchong.com']
    # start_urls = [f'http://muchong.com/f-189-{n}' for n in range(1, 201)]
    # start_urls = ['http://muchong.com/f-189-21']

    @staticmethod
    def get_start_urls():
        """ 获取起始url """
        for board_url in settings.BOARD_MAP:
            yield [f'{board_url}-{page}' for page in range(1, 201)]

    def start_requests(self):
        """ 将起始url加入请求队列 """
        for urls in self.get_start_urls():
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        posts_list = response.xpath('//tr[@class="forum_list"]')[1:]
        board = settings.BOARD_MAP[response.url.rsplit('-', maxsplit=1)[0]]
        for tr in posts_list:
            itemloader = LwwItemLoader(item=LwwPostItem(), selector=tr)
            itemloader.add_value("board_id", board[0])
            itemloader.add_value("board_name", board[1])
            itemloader.add_value("board_url", response.url)
            if tr.xpath('th[@class="thread-name"]/span/a[@class="xmc_blue"]/text()'):
                itemloader.add_xpath('tag', 'th[@class="thread-name"]/span/a[@class="xmc_blue"]/text()')
            else:
                itemloader.add_value('tag', "未知")
            itemloader.add_xpath('title', 'th[@class="thread-name"]/a[@class="a_subject"]/text()')
            itemloader.add_xpath('post_url', 'th[@class="thread-name"]/a[@class="a_subject"]/@href')
            if tr.xpath('th[@class="thread-name"]/img/following-sibling::font[1]/text()'):
                itemloader.add_xpath('coin_num', 'th[@class="thread-name"]/img/following-sibling::font[1]/text()')
            else:
                itemloader.add_value('coin_num', 0)
            if tr.xpath('th[@class="thread-name"]/span[2]'):
                itemloader.add_xpath('comment_num', 'th[@class="thread-name"]/span[2]/text()')
            else:
                itemloader.add_value('comment_num', 0)
            itemloader.add_xpath('browser_num', 'th[@class="thread-name"]/span[2]/text()')
            itemloader.add_xpath('author_name', 'th[@class="by"][1]/cite/a/text()')
            itemloader.add_xpath('author_url', 'th[@class="by"][1]/cite/a/@href')
            itemloader.add_xpath('post_time', 'string(th[@class="by"][1]/span[@class="xmc_b9"])')
            itemloader.add_xpath('last_comment_user', 'th[@class="by"][2]/span[@class="xmc_b9"]/a/text()')
            itemloader.add_xpath('last_comment_time', 'th[@class="by"][2]/cite/nobr/text()')
            post_item = itemloader.load_item()
            yield post_item

