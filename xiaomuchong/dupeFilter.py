# -*- coding:utf-8 _*-
"""
@author: Zhang Yafei
@time: 2019/11/{DAY}
"""
from scrapy.dupefilters import BaseDupeFilter
from redis import Redis, ConnectionPool
from scrapy.utils.request import request_fingerprint
from scrapy_redis.dupefilter import RFPDupeFilter
from scrapy.http.request import Request


class RedisFilter(BaseDupeFilter):
    def __init__(self):
        pool = ConnectionPool(host='127.0.0.1', port='6379')
        self.conn = Redis(connection_pool=pool)

    def request_seen(self, request):
        """
        检测当前请求是否已经被访问过
        :param request:
        :return: True表示已经访问过；False表示未访问过
        """
        fd = request_fingerprint(request=request)
        # key可以自定制
        added = self.conn.sadd('visited_urls', fd)
        return added == 0


class RedisDupeFilter(RFPDupeFilter):

    @classmethod
    def from_crawler(cls, crawler):
        """Returns instance from crawler.

        Parameters
        ----------
        crawler : scrapy.crawler.Crawler

        Returns
        -------
        RFPDupeFilter
            Instance of RFPDupeFilter.

        """
        return cls.from_settings(crawler.settings)

    def request_seen(self, request: Request) -> bool:
        """Returns True if request was already seen else False"""
        fp = self.request_fingerprint(request)
        added = self.server.sismember(self.key, fp)
        return added