# -*- coding: utf-8 -*-
import scrapy
try:
    from baseball.utils import NpbConst
    from baseball.items import ResultsItem
    from baseball.items import TeamResultsItem
except ModuleNotFoundError:
    from utils import NpbConst
    from items import ResultsItem
    from items import TeamResultsItem


class ResultsSpider(scrapy.Spider):
    name = 'results'
    allowed_domains = ['npb.jp']

    def __init__(self, year, month, day, team):
        self.day = day
        self.month = month
        self.team = team
        index = month + 1 if month == 3 else month
        i = '{:0>2}'.format(str(index))
        self.start_urls = []
        if team is not None:
            for i in range(3, 12):
                i = '{:0>2}'.format(str(i))
                self.start_urls.append(
                    f'https://npb.jp/bis/{year}/calendar/index_{i}.html')
        else:
            self.start_urls = [
                f'https://npb.jp/bis/{year}/calendar/index_{i}.html']

    def parse(self, response):
        """
        @url https://npb.jp/bis/2019/calendar/index_04.html
        @cb_kwargs {"year": "2019", "month": "4", "day": "10", "team": "None"}
        @returns items 30 30
        @returns requests 0 0
        """
        if self.team is not None:
            m = NpbConst.GET_MONTH_REG_EXP.match(response.xpath(
                '//td[@class="tenamesubtitle"]/h2/text()').extract_first())
            for i, tr in enumerate(response.xpath(
                    '//table[@class="tetblmain"]/tr')):
                if i < 1:
                    continue
                for td in tr.xpath('td'):
                    yield self._get_team_results(i, td, m)
        else:
            yield self._get_results(response)

    def _get_team_results(self, i, td, m):
        try:
            d = int(td.xpath('div[1]/a/text()').extract_first())
        except TypeError:
            return
        month = m.group(2)
        if m.group(2) == '3･4':
            if i < 4 and d > 19:
                month = '3'
            else:
                month = '4'
        dt = '-'.join([
            m.group(1),
            '{:0>2}'.format(month),
            '{:0>2}'.format(str(d))
        ])
        item = TeamResultsItem()
        item['datetime'] = dt
        abbreviation = NpbConst.TEAM_CODE_TO_ABBREVIATION.get(
            self.team)
        for div in td.xpath('div[2]/div'):
            result = div.xpath('a/text()').extract_first() or ''
            if abbreviation in result:
                item['match'] = result
                break
        for div in td.xpath('div[3]/div'):
            result = div.xpath('a/text()').extract_first() or ''
            if abbreviation in result:
                item['match'] = result
                break
        if item.get('match') is not None:
            return item

    def _get_results(self, response):
        for i, tr in enumerate(response.xpath(
                '//table[@class="tetblmain"]/tr')):
            if i < 1:
                continue
            for td in tr.xpath('td'):
                try:
                    d = int(td.xpath('div[1]/a/text()').extract_first())
                except TypeError:
                    try:
                        d = int(td.xpath('div[1]/text()').extract_first())
                    except TypeError:
                        continue
                if self.day == d:
                    item = ResultsItem()
                    item['match1'] = td.xpath(
                        'div[2]/div[1]/a/text()').extract_first()
                    item['match2'] = td.xpath(
                        'div[2]/div[2]/a/text()').extract_first()
                    item['match3'] = td.xpath(
                        'div[2]/div[3]/a/text()').extract_first()
                    if td.xpath(
                            'div[2]/div[4]/a/text()'
                            ).extract_first() is not None:
                        item['match4'] = td.xpath(
                            'div[2]/div[4]/a/text()').extract_first()
                    else:
                        item['match4'] = td.xpath(
                            'div[3]/div[1]/a/text()').extract_first()
                    item['match5'] = td.xpath(
                        'div[3]/div[2]/a/text()').extract_first()
                    item['match6'] = td.xpath(
                        'div[3]/div[3]/a/text()').extract_first()
                    return item
