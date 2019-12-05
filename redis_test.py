# -*- coding:utf-8 -*-
"""
@author: Zhang Yafei
@time: 2019/11/30
"""
from redis import Redis, ConnectionPool

# 连接池
pool = ConnectionPool(host='127.0.0.1', port=6379)
conn = Redis(connection_pool=pool)
print(conn.keys())
# print(conn.exists("post_urls"))

# 查看队列
# print(conn.lrange("charmer:items", 0, -1))
# 查看集合
print(conn.smembers('posts_urls'))
print(conn.smembers('posts_page_urls'))
# print(conn.smembers('visited_urls'))
# print(conn.smembers('dupefilter:1575163765'))
# print(conn.smembers('posts:dupefilter'))
# print(conn.smembers('comment_url'))
# comments_error = conn.smembers('comments:error')
# print(comments_error)

# 查看集合长度
# print(conn.scard("posts:dupefilter"))
print(conn.scard("comments:dupefilter"))
print(conn.scard("posts_urls"))
print(conn.scard("posts_visit_urls"))
print(conn.scard("posts_page_urls"))
# 查看集合元素
# print(conn.smembers('team:dupefilter'))
# 查看是否是集合成员
# print(conn.sismember('team:dupefilter', '9ff5702d6a40f5949a1dbd79955f999268c38761'))
# 集合运算
# print(conn.sdiff("posts_visit_urls", "posts_page_urls"))
# print(conn.sdiff("posts_page_urls", "posts_visit_urls"))
# 删除键
# conn.delete('posts:dupefilter')
conn.delete('comments:dupefilter')
# conn.delete('comments:error')
# conn.delete('comment_url')

# conn.delete('posts:error')
# conn.delete('posts_urls')
# conn.delete('posts:error')
# conn.delete('team:dupefilter')
# conn.delete("<PostsSpider 'posts' at 0x4b0fe88>:error")
# conn.flushall()
# print(conn.keys())
