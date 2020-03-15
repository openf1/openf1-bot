# Scrapy settings for motorsportmagazine project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import sys
import os

from os.path import dirname
path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(path)
path = dirname(dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(path)

BOT_NAME = 'openf1-bot.motorsportmagazine'

SPIDER_MODULES = ['motorsportmagazine.spiders']
NEWSPIDER_MODULE = 'motorsportmagazine.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'motorsportmagazine (+http://www.yourdomain.com)'

DOWNLOADER_MIDDLEWARES = {
}

ITEM_PIPELINES = {
    'motorsportmagazine.pipelines.JsonWithEncodingPipeline': 300,
}

LOG_LEVEL = 'ERROR'

DOWNLOAD_DELAY = 1
