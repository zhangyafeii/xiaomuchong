# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from redis import ConnectionPool, Redis
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.request import request_fingerprint
from scrapy.utils.project import get_project_settings
from lww.DBHelper import redis_conn
import logging

settings = get_project_settings()


class LwwSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LwwDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.conn = redis_conn
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        if response.status != 200 or not self.judge_request_response(response, spider):
            self.logger.warning(f"{request.url, response.status} 该请求返回也页面不正确, 忽略此请求")
            raise IgnoreRequest()
        else:
            fd = request_fingerprint(request=request)
            self.conn.sadd(settings["SCHEDULER_DUPEFILTER_KEY"] % {'spider': spider.name}, fd)
            return response

    def judge_request_response(self, response, spider):
        """ 判断返回页面是否正确：是否可以取到需要的数据信息 """
        if spider.name == 'team' and not response.xpath("//div[@class='solid forum_info xmc_line_lrb'][1]//div[@class='xmc_fl forum_Team'][1]/dl[1]//a"):
            return False
        elif spider.name == 'charmer' and not response.xpath('//div[@class="user_Rank bg_global  bg_global_padding"]/ul/li'):
            return False
        elif spider.name == 'post' and not response.xpath('//tr[@class="forum_list"]'):
            return False
        elif spider.name == 'comments' and not response.xpath("//tbody[starts-with(@id, 'pid')]"):
            return False
        elif spider.name == 'users' and not response.xpath('//div[@class="space_index "]//tr/td[2]/div/a/text()'):
            return False
        return True

    def process_exception(self, request, exception, spider):
        print(request.url, exception)

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
