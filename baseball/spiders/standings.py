# -*- coding: utf-8 -*-
import scrapy
try:
    from baseball.items import StandingsItem
except ModuleNotFoundError:
    from items import StandingsItem


class StandingsSpider(scrapy.Spider):
    name = 'standings'
    allowed_domains = ['npb.jp']

    def __init__(self, year, league):
        self.league = league
        self.start_urls = [f'https://npb.jp/bis/{year}/stats/']

    def parse(self, response):
        league_id = 'stdcl' if self.league == 'c' else 'stdpl'
        for rank, tr in enumerate(
                response.xpath(
                    f'//div[@id="{league_id}"]/table/tr/td/table/tr'
                    ),
                -1):
            if rank < 1:
                continue
            item = StandingsItem()
            item['rank'] = rank
            item['team'] = tr.xpath('td[1]/text()').extract_first()
            item['games'] = tr.xpath('td[2]/text()').extract_first()
            item['win'] = tr.xpath('td[3]/text()').extract_first()
            item['lose'] = tr.xpath('td[4]/text()').extract_first()
            item['draw'] = tr.xpath('td[5]/text()').extract_first()
            item['w_per'] = tr.xpath('td[6]/text()').extract_first()
            item['gb'] = tr.xpath('td[7]/text()').extract_first() or ''
            yield item
