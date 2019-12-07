# -*- coding: utf-8 -*-
import scrapy
from xiaomuchong.items import LwwItemLoader, LwwCommentItem
from xiaomuchong.DBHelper import db_conn, redis_conn
import pandas as pd


def get_start_urls():
    data = pd.read_sql(sql="posts", con=db_conn, columns=["post_url"])
    post_urls = data['post_url']
    callback = 'parse'
    if len(post_urls) == redis_conn.scard('comments:dupefilter'):
        redis_conn.delete('comments:dupefilter')
        post_urls = redis_conn.smembers('posts_page_urls')
        callback = 'parse_detail'
    elif len(post_urls) < redis_conn.scard('comments:dupefilter'):
        post_urls = redis_conn.smembers('posts_page_urls')
        post_urls = [url.decode() for url in post_urls]
        callback = 'parse_detail'
    return post_urls, callback

# def get_start_urls():
#     post_urls = redis_conn.smembers('posts_page_urls')
#     post_urls = [url.decode() for url in post_urls]
#     callback = 'parse_detail'
#     return post_urls, callback


class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['muchong.com']
    # start_urls = ['http://muchong.com/t-13667321-1']
    # start_urls = get_start_urls()

    def start_requests(self):
        # url需要从数据库中提取
        start_urls, callback = get_start_urls()
        callback = self.parse if callback == 'parse' else self.parse_detail
        for url in start_urls:
            yield scrapy.Request(url=url, callback=callback)

    def parse(self, response):
        """ 评论表将获取所有帖子page_url并存入redis """
        request_url = response.url[:-1]
        page_nums = int(response.xpath('//div[@class="xmc_fr xmc_Pages"]//td[2]/text()').extract_first().split('/')[1])
        if page_nums > 1:
            for page in range(1, int(page_nums) + 1):
                redis_conn.sadd('posts_page_urls', request_url + str(page))
        else:
            redis_conn.sadd('posts_page_urls', response.url)

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
            if '1楼' in tbody.xpath('tr/td[@class="pls_foot"]/div/span/a/text()').extract_first():
                item_loader.add_value("isTopic", 1)
            else:
                item_loader.add_value("isTopic", 0)
            comment_item = item_loader.load_item()
            yield comment_item