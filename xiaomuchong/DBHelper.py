# -*- coding:utf-8 _*-
"""
@author:Zhang Yafei
@time: 2019/12/02
"""
import pandas as pd
from redis import ConnectionPool, Redis
from scrapy.utils.project import get_project_settings
from DBUtils.PooledDB import PooledDB
import psycopg2
from xiaomuchong import settings
from sqlalchemy import create_engine


class DBPoolHelper(object):
    def __init__(self, type=None):
        """
        # sqlite3
        # 连接数据库文件名，sqlite不支持加密，不使用用户名和密码
        import sqlite3
        config = {"datanase": "path/to/your/dbname.db"}
        pool = PooledDB(sqlite3, maxcached=50, maxconnections=1000, maxusage=1000, **config)
        # mysql
        import pymysql
        pool = PooledDB(pymysql,5,host='localhost', user='root',passwd='pwd',db='myDB',port=3306) #5为连接池里的最少连接数
        # postgressql
        import psycopg2
        POOL = PooledDB(creator=psycopg2, host="127.0.0.1", port="5342", user, password, database)
        # sqlserver
        import pymssql
        pool = PooledDB(creator=pymssql, host=host, port=port, user=user, password=password, database=database, charset="utf8")
        :param type:
        """
        POOL = PooledDB(
            creator=psycopg2,  # 使用链接数据库的模块
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            host=settings.POSTGRESQL_HOST,
            port=settings.POSTGRESQL_PORT,
            user=settings.POSTGRESQL_USER,
            password=settings.POSTGRESQL_PASSWORD,
            database=settings.POSTGRESQL_DATABASE,
        )
        self.conn = POOL.connection()
        self.cursor = self.conn.cursor()

    def connect_close(self):
        """关闭连接"""
        self.cursor.close()
        self.conn.close()

    def execute(self, sql, params=tuple()):
        self.cursor.execute(sql, params)  # 执行这个语句
        self.conn.commit()

    def fetchone(self, sql, params=tuple()):
        self.cursor.execute(sql, params)
        data = self.cursor.fetchone()
        return data

    def fetchall(self, sql, params=tuple()):
        self.cursor.execute(sql, params)
        data = self.cursor.fetchall()
        return data


def pandas_db_helper():
    """
    'postgresql://postgres:0000@127.0.0.1:5432/xiaomuchong'
    "mysql+pymysql://root:0000@127.0.0.1:3306/srld?charset=utf8mb4"
    "sqlite: ///sqlite3.db"
    """
    engine = create_engine(settings.DATABASE_ENGINE)
    conn = engine.connect()
    return conn


def redis_init():
    settings = get_project_settings()
    if settings["REDIS_PARAMS"]:
        pool = ConnectionPool(host=settings["REDIS_HOST"], port=settings["REDIS_PORT"],
                              password=settings["REDIS_PARAMS"]['password'])
    else:
        pool = ConnectionPool(host=settings["REDIS_HOST"], port=settings["REDIS_PORT"])
    conn = Redis(connection_pool=pool)
    return conn


redis_conn = redis_init()
db_conn = pandas_db_helper()


if __name__ == '__main__':
    # db = DBPoolHelper()
    # res = db.fetchall("select * from team")
    # print(res)
    db2 = pandas_db_helper()
    # data = pd.read_sql_table("team", con=db2, index_col="board_id")
    # data = pd.read_sql(sql="select board_name, board_id from team", con=db_conn)
    # name, url = data['board_name'], data['board_id']
    # data = pd.read_sql(sql="select post_url from posts", con=db_conn)
    data = pd.read_sql(sql="posts", con=db_conn, columns=["post_url"])
    print(data['post_url'])