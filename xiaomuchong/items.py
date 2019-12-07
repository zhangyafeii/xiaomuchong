# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from urllib.parse import urljoin


class TakeFirstCustom(TakeFirst):
    def __call__(self, values):
        for value in values:
            return value


class LwwItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    # default_output_processor = TakeFirstCustom()


def date_convert(value):
    value = value[0].strip() if type(value) == list else value.strip()
    date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
    return date


def datetime_convert(value):
    value = value[0].strip("\r\n").strip()
    date_time = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return date_time


def url_join(value):
    if type(value) is str:
        return urljoin('http://muchong.com', value)
    return urljoin('http://muchong.com', value[0])


def url_bbs_join(value):
    if type(value) is str:
        uid = re.search("uid=(\d+)", value).group(1)
    else:
        uid = re.search("uid=(\d+)", value[0]).group(1)
    return f'http://muchong.com/bbs/space.php?uid={uid}'


class LwwTeamItem(scrapy.Item):
    """ Team表 """
    board_id = scrapy.Field()
    board_name = scrapy.Field()
    header_name = scrapy.Field(input_processor=Join(' | '))
    header_url = scrapy.Field(
        input_processor=MapCompose(url_bbs_join),
        output_processor=Join('||'),
    )
    moderator = scrapy.Field(input_processor=Join(' | '), )
    moderator_url = scrapy.Field(input_processor=MapCompose(url_bbs_join), output_processor=Join('||'))
    attendance = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into team(board_id, board_name, header_name, header_url, moderator, moderator_url, attendance)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (self['board_id'], self["board_name"], self["header_name"], self["header_url"], self["moderator"],
                  self["moderator_url"], self["attendance"])
        return insert_sql, params


class LwwCharmerItem(scrapy.Item):
    """ charmer表 """
    board_id = scrapy.Field()
    board_name = scrapy.Field()
    charmer_name = scrapy.Field()
    effect_index = scrapy.Field()
    charmer_url = scrapy.Field(output_processor=url_bbs_join)

    def get_insert_sql(self):
        insert_sql = """
            insert into charmer(board_id, board_name, charmer_name, effect_index, charmer_url)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (self['board_id'], self['board_name'], self['charmer_name'], self['effect_index'], self['charmer_url'])
        return insert_sql, params


def get_comment_num(value):
    if type(value[0]) == int:
        return value
    res = value[0].strip('(').strip(')').split('/')[0] if value else 0
    return res


def get_browser_num(value):
    res = value[0].strip('(').strip(')').split('/')[1] if value else 0
    return res


def get_coin_num(value):
    # if "OCI" in value:
    #     value = re.search("OCI+(\d+).*?", value)
    return int(value)


class LwwPostItem(scrapy.Item):
    """ Post表 """
    board_id = scrapy.Field()
    board_name = scrapy.Field()
    board_url = scrapy.Field()
    tag = scrapy.Field()
    title = scrapy.Field()
    post_url = scrapy.Field(input_processor=url_join)
    coin_num = scrapy.Field(iutput_processor=MapCompose(get_coin_num))
    comment_num = scrapy.Field(input_processor=get_comment_num)
    browser_num = scrapy.Field(input_processor=get_browser_num)
    author_name = scrapy.Field()
    author_url = scrapy.Field(output_processor=url_bbs_join)
    post_time = scrapy.Field(output_processor=date_convert)
    last_comment_user = scrapy.Field()
    last_comment_time = scrapy.Field(output_processor=datetime_convert)

    def get_insert_sql(self):
        insert_sql = """
            insert into posts(board_id, board_name, board_url, tag, title, post_url, coin_num, comment_num, browser_num, 
            author_name, author_url, post_time, last_comment_user, last_comment_time)
            VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s,%s,%s,%s)
        """
        params = (self['board_id'], self['board_name'], self['board_url'], self['tag'], self['title'], self['post_url'],
                  self['coin_num'], self['comment_num'], self['browser_num'],
                  self['author_name'], self['author_url'], self['post_time'], self['last_comment_user'],
                  self['last_comment_time'])
        return insert_sql, params


def process_content(content):
    text = content[0].replace("\n", "").strip().replace("发自小木虫IOS客户端", "").replace("发自小木虫Android客户端", "")
    return text


def get_praise_num(value):
    res = int(value[0].strip(" 赞一下(").strip("人)")) if value[0] != 0 and value[0] != " 赞一下" else 0
    return res


class LwwCommentItem(scrapy.Item):
    """ comment 表 """
    post_url = scrapy.Field()  # 主题帖url
    author_name = scrapy.Field()  # 作者姓名
    author_url = scrapy.Field(output_processor=url_bbs_join)  # 作者url
    post_time = scrapy.Field(output_processor=datetime_convert)  # 发帖时间
    reference = scrapy.Field()  # 是否引用
    content = scrapy.Field(output_processor=process_content)  # 帖子内容
    praise_num = scrapy.Field(output_processor=get_praise_num)  # 点赞数
    floor = scrapy.Field()  # 楼层
    isTopic = scrapy.Field()  # 是否是主题帖

    def get_insert_sql(self):
        insert_sql = """
            insert into comment(post_url, author_name, author_url, post_time, reference, content, praise_num, floor, isTopic) 
            VALUES (%s, %s, %s, %s,%s,%s, %s, %s, %s)
        """
        params = (self['post_url'], self['author_name'], self['author_url'], self['post_time'],
                  self['reference'], self['content'], self['praise_num'], self['floor'], self['isTopic'])
        return insert_sql, params


def get_listener(value):
    return int(re.search('听众:(\d+)', value[0]).group(1))


def get_red_flower(value):
    return int(re.search('红花:(\d+)', value[0]).group(1))


class LwwUserItem(scrapy.Item):
    """ User表 """
    user_name = scrapy.Field()
    user_url = scrapy.Field()
    listener = scrapy.Field(output_processor=get_listener)
    red_flower = scrapy.Field(output_processor=get_red_flower)
    register_time = scrapy.Field(input_processor=datetime_convert)
    last_active_time = scrapy.Field(input_processor=datetime_convert)
    last_post_time = scrapy.Field(input_processor=datetime_convert)
    serial_num = scrapy.Field()
    user_group = scrapy.Field()
    help = scrapy.Field(input_processor=MapCompose(int))
    vip = scrapy.Field(input_processor=MapCompose(float))
    gold = scrapy.Field(input_processor=MapCompose(float))
    spend = scrapy.Field(input_processor=MapCompose(int))
    soft = scrapy.Field(input_processor=MapCompose(int))
    posts = scrapy.Field(input_processor=MapCompose(int))
    rule = scrapy.Field()
    online = scrapy.Field()
    online_status = scrapy.Field()
    major = scrapy.Field()
    gender = scrapy.Field()
    region = scrapy.Field()
    birthday = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO users(user_name, user_url, listener,red_flower,register_time,last_active_time,last_post_time, serial_num, user_group, help, vip,gold,spend,soft,posts,rule,online,online_status,major,gender,region,birthday
            ) VALUES (%s, %s, %s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s)
        """
        params = (
            self['user_name'], self['user_url'], self['listener'], self['red_flower'], self['register_time'],
            self['last_active_time'], self['last_post_time'],
            self['serial_num'], self['user_group'], self['help'], self['vip'], self['gold'], self['spend'],
            self['soft'],
            self['posts'], self['rule'], self['online'],
            self['online_status'], self['major'], self['gender'], self['region'], self['birthday']
        )
        return insert_sql, params
