# -*- coding:utf-8 _*-
"""
@author: Zhang Yafei
@time: 2019/11/30
"""
import os
import sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(__file__))


def run(job):
    execute(['scrapy', 'crawl', job])
    # execute(['scrapy', 'crawl', job, "--nolog"])


if __name__ == '__main__':
    # run(job="team")
    # run(job="charmer")
    run(job="posts")
    # run(job="comments")
    # run(job="users")
