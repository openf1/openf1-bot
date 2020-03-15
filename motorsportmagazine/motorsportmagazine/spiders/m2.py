import json

from logzero import logger
from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.exceptions import NotSupported
from scrapy.linkextractors import LinkExtractor as sle

from filters import UrlFilter
from misc.spider import CommonSpider


class M2Spider(CommonSpider):
    name = "m2"
    base_url = 'https://database.motorsportmagazine.com'
    start_urls = [
        f'{base_url}/database/'
    ]
    valid_categories = [
        'drivers',
        #'teams',
    ]
    allow_rules = ['/' + i + '$' for i in valid_categories]
    rules = [
        Rule(sle(allow=allow_rules), callback='parse_filter', follow=True),
    ]

    filter_css_rules = {
        'category': '.content-title > h1::text',
        'url': '.facetapi-inactive ::attr(href)',
    }

    content_css_rules = {
        'tbody .views-field-field-person-surname': {
            'name': 'a:last-child::text',
            'url': 'a:last-child::attr(href)',
        }
    }

    def parse_filter(self, response):
        logger.info(f'Response from {response.url}')

        x = self.parse_with_rules(response, self.filter_css_rules, dict)
        try:
            uf = UrlFilter.create_filter(x)
            url = uf.apply()
            if not url:
                raise ValueError(
                    "Can't apply filter, no URL found"
                )
            url = self.base_url + url
            logger.info(f'Redirect to {url}')
            yield Request(url, callback=self.parse_list)
        except ValueError as err:
            logger.exception(err)

    def parse_list(self, response):
        logger.info(f'Response from {response.url}')

        x = self.parse_with_rules(response, self.content_css_rules, dict)
