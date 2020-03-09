from logzero import logger
from scrapy.spiders import CrawlSpider


class templateSpider(CrawlSpider):
    name = "template"
    allowed_domains = ["template.com"]
    start_urls = [
        "http://www.template.com/",
    ]

    def parse(self, response):
        logger.info('Parse ' + response.url)
