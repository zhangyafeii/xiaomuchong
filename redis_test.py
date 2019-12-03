# -*- coding:utf-8 _*-
"""
@author: Zhang Yafei
@time: 2019/11/30
"""
from redis import Redis, ConnectionPool

# 连接池
pool = ConnectionPool(host='127.0.0.1', port=6379)
conn = Redis(connection_pool=pool)
print(conn.keys())
# 查看队列
# print(conn.lrange("charmer:items", 0, -1))
# 查看集合
# print(conn.smembers('visited_urls'))
# print(conn.smembers('dupefilter:1575163765'))
# print(conn.smembers('posts:dupefilter'))

# 查看集合长度
# print(conn.scard("posts:dupefilter"))
# 查看集合元素
# print(conn.smembers('team:dupefilter'))
# 查看是否是集合成员
# print(conn.sismember('team:dupefilter', '9ff5702d6a40f5949a1dbd79955f999268c38761'))
# 删除键
# conn.delete('posts:dupefilter')

# conn.delete('posts:error')
# conn.delete('team:dupefilter')
# conn.delete("<PostsSpider 'posts' at 0x4b0fe88>:error")
# conn.flushall()
# print(conn.keys())
