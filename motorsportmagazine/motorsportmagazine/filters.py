from collections import namedtuple
from logzero import logger
from urllib import parse


class UrlFilter(object):
    def __init__(self, data):
        self.data = data

    @staticmethod
    def create_filter(data):
        if 'category' not in data:
            raise ValueError('Can\'t select filter: no category')    

        category = data.pop('category')
        if len(category) == 0:
            raise ValueError('Can\'t select filter: empty category')
        category = category[0].strip()

        F = {
            'Drivers/Riders': DriversUrlFilter,
            'Teams': TeamsUrlFilter,
        }.get(category, None)

        if not F:
            raise ValueError(f'Can\'t select filter: unknown category \'{category}\'')

        return F(data)

    def _deal_qs(self, qs):
        query = namedtuple('query', 'filter_by, value')
        d = dict(parse.parse_qsl(qs))        

        for v in d.values():
            filter_by, value = v.split(':')
            query.filter_by = filter_by
            query.value = value

        return query

    def apply(self):
        logger.info(f"Apply filter '{self.filter_by}={self.value}'")

        if 'url' not in self.data:
            raise ValueError('Can\'t apply URL filter: no URL found in items')
        
        for url in self.data.get('url'):
            url = parse.unquote(url)
            qs = self._deal_qs(parse.urlsplit(url).query)

            if (qs.filter_by == self.filter_by) and (qs.value == self.value):
                return url

        return None


class DriversUrlFilter(UrlFilter):
    filter_by = 'person_championship_series'
    value = 'F1'


class TeamsUrlFilter(UrlFilter):
    filter_by = 'team_championpships'
    value = 'F1 World Championship'
