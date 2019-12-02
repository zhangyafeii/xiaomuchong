# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from twisted.enterprise import adbapi


class PostgresSQLPipeline(object):
    """ PostgreSQL pipeline class """

    def __init__(self, dbpool):
        self.logger = logging.getLogger()
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['POSTGRESQL_HOST'],
            database=settings['POSTGRESQL_DATABASE'],
            user=settings['POSTGRESQL_USER'],
            password=settings['POSTGRESQL_PASSWORD'],
        )
        dbpool = adbapi.ConnectionPool('psycopg2', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._insert_item, item)
        d.addErrback(self._handle_error, item, spider)

    def _insert_item(self, cursor, item):
        """Perform an insert or update."""
        insert_sql, params = item.get_insert_sql()
        try:
            cursor.execute(insert_sql, params)
            print('插入成功')
        except Exception as e:
            self.logger.error('插入失败', e)

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        self.logger.error(failure)
        # self.logger.error(failure, failure.printTraceback())