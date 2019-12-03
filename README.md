## README 操作说明
### 一、 安装依赖包
-  在命令行下进入项目目录
- 1.使用虚拟环境
```python
pipenv install
pipenv shell
```
![激活虚拟环境](image/激活虚拟环境.png)
- 2.使用本地环境
```angular2
pip install -r requirements.txt
```
### 二、项目前期配置
> - Cookie的配置
```python
COOKIES_ENABLED = False
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Cookie': '_ga=GA1.2.1170985894.1574990237; Hm_lvt_2207ecfb7b2633a3bc5c4968feb58569=1574990237; _emuch_index=1; _discuz_uid=19112081; _discuz_pw=14e6e4e1bc563282; last_ip=59.49.101.213_19112081; discuz_tpl=qing; _last_fid=189; _discuz_cc=38751939948397088; view_tid=13768047; Hm_lpvt_2207ecfb7b2633a3bc5c4968feb58569=1574990695',
}
```
> - 数据库的配置
```python
POSTGRESQL_HOST = "127.0.0.1"
POSTGRESQL_DATABASE = "xiaomuchong"
POSTGRESQL_USER = "postgres"
POSTGRESQL_PASSWORD = "0000"
POSTGRESQL_PORT = "5432"
DATABASE_ENGINE = 'postgresql://postgres:0000@127.0.0.1:5432/xiaomuchong'
```
> 在postgressql中创建数据库xiaomuchong,并在xiaomuchong中新建五张表，具体表名称和字段参照items.py文件,我这已经创建了三张表，你可以直接复制创建
```sql
-- Database: xiaomuchong
-- DROP DATABASE xiaomuchong;

CREATE DATABASE xiaomuchong
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Chinese (Simplified)_People''s Republic of China.936'
    LC_CTYPE = 'Chinese (Simplified)_People''s Republic of China.936'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
- 
CREATE TABLE public.team
(
    board_id bigint NOT NULL,
    board_name character varying COLLATE pg_catalog."default",
    header_name character varying COLLATE pg_catalog."default",
    header_url character varying COLLATE pg_catalog."default",
    moderator character varying COLLATE pg_catalog."default",
    moderator_url character varying COLLATE pg_catalog."default",
    attendance character varying COLLATE pg_catalog."default",
    CONSTRAINT team_pkey PRIMARY KEY (board_id)
)
CREATE TABLE public.charmer
(
    board_id bigint NOT NULL,
    board_name character varying COLLATE pg_catalog."default",
    charmer_name character varying COLLATE pg_catalog."default",
    charmer_url character varying COLLATE pg_catalog."default" NOT NULL,
    effect_index character(10) COLLATE pg_catalog."default",
    CONSTRAINT charmer_pkey PRIMARY KEY (charmer_url)
)

CREATE TABLE public.posts
(
    board_id bigint NOT NULL,
    board_name character varying COLLATE pg_catalog."default",
    board_url character varying COLLATE pg_catalog."default",
    tag character varying COLLATE pg_catalog."default",
    title character varying COLLATE pg_catalog."default",
    post_url character varying COLLATE pg_catalog."default" NOT NULL,
    comment_num bigint,
    browser_num bigint,
    author_name character varying COLLATE pg_catalog."default",
    author_url character varying COLLATE pg_catalog."default",
    post_time date,
    last_comment_user character varying COLLATE pg_catalog."default",
    last_comment_time timestamp without time zone,
    coin_num bigint,
    CONSTRAINT posts_pkey PRIMARY KEY (post_url)
)


```
> - scrapy_redis的配置
```python
# 方式四： 修改调度器
REDIS_HOST = '127.0.0.1'                            # 主机名
REDIS_PORT = 6379                                   # 端口
# REDIS_PARAMS  = {'password':'0000'}                 # Redis连接参数             默认：REDIS_PARAMS = {'socket_timeout': 30,'socket_connect_timeout': 30,'retry_on_timeout': True,'encoding': REDIS_ENCODING,}）
REDIS_ENCODING = "utf-8"

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS ='scrapy_redis.dupefilter.RFPDupeFilter'
# DEPTH_PRIORITY = 1  # 广度优先
# DEPTH_PRIORITY = -1 # 深度优先
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'  # 默认使用优先级队列（默认），其他：PriorityQueue（有序集合），FifoQueue（列表）、LifoQueue（列表）
# 广度优先
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
# 深度优先
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'
SCHEDULER_QUEUE_KEY = '%(spider)s:requests'  # 调度器中请求存放在redis中的key
SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"  # 对保存到redis中的数据进行序列化，默认使用pickle
SCHEDULER_PERSIST = True  # 是否在关闭时候保留原来的调度器和去重记录，True=保留，False=清空
SCHEDULER_FLUSH_ON_START = False  # 是否在开始之前清空 调度器和去重记录，True=清空，False=不清空
SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'  # 去重规则，在redis中保存时对应的key
# 优先使用DUPEFILTER_CLASS，如果么有就是用SCHEDULER_DUPEFILTER_CLASS
# SCHEDULER_DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'  # 去重规则对应处理的类
```
> 只需要修改你电脑上redis的配置
### 三、项目运行
- 项目结构介绍 
```
E:.
│  main.py
│  README.md
│  redis_test.py
│  requirements.txt
│  scrapy.cfg
│
└─lww
    │  DBHelper.py
    │  dupeFilter.py
    │  extensions.py
    │  items.py
    │  middlewares.py
    │  pipelines.py
    │  settings.py
    │
    └─spiders
            charmer.py
            comments.py
            posts.py
            team.py
            users.py
            __init__.py
```
- 项目运行命令
> 进入项目目录,运行main.py文件,或者执行
```python
scrapy crawl spider_name   # 爬虫名称 team|charmer|posts|comments|users
```
![执行命令](image/执行命令.png)
- 前三个爬虫可以直接运行，commments和users的urls需要从数据库中抽取，所以需要等到posts下载完


