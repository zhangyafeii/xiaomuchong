# -*- coding:utf-8 _*-
"""
@author:Zhang Yafei
@time: 2019/12/01
"""
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.request import request_fingerprint
from xiaomuchong.DBHelper import redis_conn
from xiaomuchong import settings


class MyExtension(object):
    def __init__(self):
        self.conn = redis_conn

    @classmethod
    def from_crawler(cls, crawler):
        self = cls()
        # crawler.signals.connect(self.response_received, signal=signals.response_received)
        crawler.signals.connect(self.spider_error, signal=signals.spider_error)
        return self

    def response_received(self, response, request, spider):
        if response.status != 200:
            self.logger.warning(f"{request.url, response.status} 该请求返回也页面不正确, 忽略此请求")
            # return request
            raise IgnoreRequest()
        else:
            fd = request_fingerprint(request=request)
            self.conn.sadd(settings.SCHEDULER_DUPEFILTER_KEY % {'spider': spider.name}, fd)

    def spider_error(self, failure, response, spider):
        print(response.url, failure)
        self.conn.sadd(f"{spider.name}:error", response.url)
        spider.crawler.engine.close_spider(spider)

