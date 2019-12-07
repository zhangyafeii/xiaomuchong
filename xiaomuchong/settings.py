# -*- coding: utf-8 -*-

# Scrapy settings for xiaomuchong project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xiaomuchong'

SPIDER_MODULES = ['xiaomuchong.spiders']
NEWSPIDER_MODULE = 'xiaomuchong.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Host': 'muchong.com',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.2.330385224.1532347235; bdshare_firstime=1532347235167; _emuch_index=1; _discuz_uid=19112081; _discuz_pw=14e6e4e1bc563282; discuz_tpl=qing; _last_fid=189; view_tid=3406533; Hm_lvt_2207ecfb7b2633a3bc5c4968feb58569=1574852456,1575193351,1575201193,1575249639; last_ip=59.49.101.213_19112081; _discuz_cc=82751688258287332; Hm_lpvt_2207ecfb7b2633a3bc5c4968feb58569=1575283787',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'xiaomuchong.middlewares.LwwSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'xiaomuchong.middlewares.LwwDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
   # 'scrapy.extensions.telnet.TelnetConsole': None,
   #  'xiaomuchong.extensions.MyExtension': 200,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'xiaomuchong.pipelines.LwwPipeline': 300,
    'xiaomuchong.pipelines.PostgresSQLPipeline': 300,
    # 'scrapy_redis_bloomfilter.pipelines.RedisPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

CLOSESPIDER_ERRORCOUNT = 1

BOARD_MAP = {
    "http://muchong.com/f-189": [0, "有机交流"],
    "http://muchong.com/f-233": [1, "微米与纳米"],
    "http://muchong.com/f-291": [2, "第一性原理"],
    "http://muchong.com/f-272": [3, "金融投资"],
    "http://muchong.com/f-452": [4, "数理科学综合"],
}

POSTGRESQL_HOST = "127.0.0.1"
POSTGRESQL_DATABASE = "xiaomuchong"
POSTGRESQL_USER = "postgres"
POSTGRESQL_PASSWORD = "0000"
POSTGRESQL_PORT = "5432"

DATABASE_ENGINE = 'postgresql://postgres:0000@127.0.0.1:5432/xiaomuchong'

# REDIRECT_ENABLED = False   # 不允许重定向

# #################################### scrapy实现redis缓存去重 ############################################
# 方式一：修改DUPEFILTER_CLASS
# DUPEFILTER_CLASS = "xiaomuchong.dupeFilter.RedisFilter"

# 方式二： 利用scrapy_redis实现去重，缺点：无法修改key
# 默认的redis配置  127.0.0.1 6379 若相同，则可以不配置
# REDIS_HOST = '127.0.0.1'                            # 主机名
# REDIS_PORT = 6379                                   # 端口
# REDIS_PARAMS  = {'password':'0000'}                 # Redis连接参数             默认：REDIS_PARAMS = {'socket_timeout': 30,'socket_connect_timeout': 30,'retry_on_timeout': True,'encoding': REDIS_ENCODING,}）
# REDIS_ENCODING = "utf-8"                            # redis编码类型             默认：'utf-8'
# # REDIS_URL = 'redis://user:pass@hostname:9001'       # 连接URL（优先于以上配置）
# DUPEFILTER_CLASS ='scrapy_redis.dupefilter.RFPDupeFilter'

# 方式三: 自定义scrapy_redis去重类，修改key
# REDIS_HOST = '127.0.0.1'                            # 主机名
# REDIS_PORT = 6379                                   # 端口
# REDIS_PARAMS  = {'password':'0000'}                 # Redis连接参数             默认：REDIS_PARAMS = {'socket_timeout': 30,'socket_connect_timeout': 30,'retry_on_timeout': True,'encoding': REDIS_ENCODING,}）
# REDIS_ENCODING = "utf-8"
# DUPEFILTER_CLASS ='xiaomuchong.dupeFilter.RedisDupeFilter'

# 方式四： 修改调度器
REDIS_HOST = '127.0.0.1'                            # 主机名
REDIS_PORT = 6379                                   # 端口
# REDIS_PARAMS = {'password':'0000'}                 # Redis连接参数             默认：REDIS_PARAMS = {'socket_timeout': 30,'socket_connect_timeout': 30,'retry_on_timeout': True,'encoding': REDIS_ENCODING,}）
REDIS_ENCODING = "utf-8"

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# DUPEFILTER_CLASS ='scrapy_redis.dupefilter.RFPDupeFilter'
DUPEFILTER_CLASS ='xiaomuchong.dupeFilter.RedisDupeFilter'
# DEPTH_PRIORITY = 1  # 广度优先
# DEPTH_PRIORITY = -1 # 深度优先
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'  # 默认使用优先级队列（默认），其他：PriorityQueue（有序集合），FifoQueue（列表）、LifoQueue（列表）
# 广度优先
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
# 深度优先
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'
SCHEDULER_QUEUE_KEY = '%(spider)s:requests'  # 调度器中请求存放在redis中的key
SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"  # 对保存到redis中的数据进行序列化，默认使用pickle
SCHEDULER_PERSIST = True  # 是否在关闭时候保留原来的调度器和去重记录，True=保留，False=清空
SCHEDULER_FLUSH_ON_START = False  # 是否在开始之前清空 调度器和去重记录，True=清空，False=不清空
SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'  # 去重规则，在redis中保存时对应的key
# 优先使用DUPEFILTER_CLASS，如果么有就是用SCHEDULER_DUPEFILTER_CLASS
# SCHEDULER_DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'  # 去重规则对应处理的类


