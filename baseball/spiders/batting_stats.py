# -*- coding: utf-8 -*-
import scrapy
try:
    from baseball.utils import NpbConst
    from baseball.items import BattingStatsItem
except ModuleNotFoundError:
    from utils import NpbConst
    from items import BattingStatsItem


class BattingStatsSpider(scrapy.Spider):
    name = 'batting_stats'
    allowed_domains = ['npb.jp']

    def __init__(self, year, team, name, league):
        self.year = year
        self.player_name = name
        self.team_name = NpbConst.TEAMS.get(team)
        self.start_urls = []
        if self.player_name is not None and self.team_name is not None:
            for i in range(2005, year + 1):
                self.start_urls.append(
                    f'https://npb.jp/bis/{i}/stats/idb1_{team}.html'
                )
        elif self.player_name is not None and self.team_name is None:
            for i in range(2005, year + 1):
                for t in NpbConst.TEAMS.keys():
                    self.start_urls.append(
                        f'https://npb.jp/bis/{i}/stats/idb1_{t}.html'
                    )
        elif self.team_name is None:
            if league is None:
                self.start_urls = [
                    f'https://npb.jp/bis/{year}/stats/bat_c.html',
                    f'https://npb.jp/bis/{year}/stats/bat_p.html',
                ]
            else:
                self.start_urls = [
                    f'https://npb.jp/bis/{year}/stats/bat_{league}.html']
        else:
            self.start_urls = [
                f'https://npb.jp/bis/{year}/stats/idb1_{team}.html']

    def parse(self, response):
        for tr in response.xpath('//*[@id="stdivmaintbl"]/table/tr'):
            if self.team_name is not None or self.player_name is not None:
                yield self._get_personal_batting_stats(response, tr)
            else:
                yield self._get_season_batting_stats(response, tr)

    def _get_personal_batting_stats(self, response, tr):
        item = BattingStatsItem()
        if not tr.xpath('td[2]/text()').extract_first():
            return
        item['name'] = tr.xpath(
            'td[2]/text()').extract_first().replace('\u3000', ' ')
        if self.player_name is not None and \
                self.player_name not in item['name']:
            return
        item['year'] = int(response.xpath(
            '/html/head/title/text()').extract_first()[0:4])
        m = NpbConst.GET_TEAM_CODE_REG_EXP.match(response.xpath(
            '//*[@id="stdivtitle"]/h1/a[2]/@href').extract_first())
        item['team'] = NpbConst.TEAMS[m.group(1)]
        item['games'] = int(tr.xpath('td[3]/text()').extract_first())
        item['pa'] = int(tr.xpath('td[4]/text()').extract_first())
        item['ab'] = int(tr.xpath('td[5]/text()').extract_first())
        item['run'] = int(tr.xpath('td[6]/text()').extract_first())
        item['hit'] = int(tr.xpath('td[7]/text()').extract_first())
        item['double'] = int(tr.xpath('td[8]/text()').extract_first())
        item['triple'] = int(tr.xpath('td[9]/text()').extract_first())
        item['hr'] = int(tr.xpath('td[10]/text()').extract_first())
        item['tb'] = int(tr.xpath('td[11]/text()').extract_first())
        item['rbi'] = int(tr.xpath('td[12]/text()').extract_first())
        item['sb'] = int(tr.xpath('td[13]/text()').extract_first())
        item['cs'] = int(tr.xpath('td[14]/text()').extract_first())
        if (item['sb'] + item['cs']) != 0:
            item['sbp'] = round(
                item['sb'] / (item['sb'] + item['cs']), 3)
        else:
            item['sbp'] = 0.000
        item['sh'] = int(tr.xpath('td[15]/text()').extract_first())
        item['sf'] = int(tr.xpath('td[16]/text()').extract_first())
        item['bb'] = int(tr.xpath('td[17]/text()').extract_first())
        item['ibb'] = int(tr.xpath('td[18]/text()').extract_first())
        item['hbp'] = int(tr.xpath('td[19]/text()').extract_first())
        item['so'] = int(tr.xpath('td[20]/text()').extract_first())
        item['dp'] = int(tr.xpath('td[21]/text()').extract_first())
        item['ba'] = round(
            float(tr.xpath('td[22]/text()').extract_first()), 3)
        item['slg'] = round(
            float(tr.xpath('td[23]/text()').extract_first()), 3)
        item['obp'] = round(
            float(tr.xpath('td[24]/text()').extract_first()), 3)
        item['ops'] = round(item['slg'] + item['obp'], 3)
        return item

    def _get_season_batting_stats(self, response, tr):
        item = BattingStatsItem()
        if not tr.xpath('td[2]/text()').extract_first():
            return
        item['year'] = int(response.xpath(
            '/html/head/title/text()').extract_first()[0:4])
        item['name'] = tr.xpath(
            'td[2]/text()').extract_first().replace('\u3000', ' ')
        if self.player_name is not None and \
                self.player_name not in item['name']:
            return
        item['team'] = NpbConst.ABBREVIATION_TEAMS.get(
            tr.xpath('td[3]/text()').extract_first())
        item['ba'] = round(
            float(tr.xpath('td[4]/text()').extract_first()), 3)
        item['games'] = int(tr.xpath('td[5]/text()').extract_first())
        item['pa'] = int(tr.xpath('td[6]/text()').extract_first())
        item['ab'] = int(tr.xpath('td[7]/text()').extract_first())
        item['run'] = int(tr.xpath('td[8]/text()').extract_first())
        item['hit'] = int(tr.xpath('td[9]/text()').extract_first())
        item['double'] = int(tr.xpath('td[10]/text()').extract_first())
        item['triple'] = int(tr.xpath('td[11]/text()').extract_first())
        item['hr'] = int(tr.xpath('td[12]/text()').extract_first())
        item['tb'] = int(tr.xpath('td[13]/text()').extract_first())
        item['rbi'] = int(tr.xpath('td[14]/text()').extract_first())
        item['sb'] = int(tr.xpath('td[15]/text()').extract_first())
        item['cs'] = int(tr.xpath('td[16]/text()').extract_first())
        if (item['sb'] + item['cs']) != 0:
            item['sbp'] = round(
                item['sb'] / (item['sb'] + item['cs']), 3)
        else:
            item['sbp'] = 0.000
        item['sh'] = int(tr.xpath('td[17]/text()').extract_first())
        item['sf'] = int(tr.xpath('td[18]/text()').extract_first())
        item['bb'] = int(tr.xpath('td[19]/text()').extract_first())
        item['ibb'] = int(tr.xpath('td[20]/text()').extract_first())
        item['hbp'] = int(tr.xpath('td[21]/text()').extract_first())
        item['so'] = int(tr.xpath('td[22]/text()').extract_first())
        item['dp'] = int(tr.xpath('td[23]/text()').extract_first())
        item['slg'] = round(
            float(tr.xpath('td[24]/text()').extract_first()), 3)
        item['obp'] = round(
            float(tr.xpath('td[25]/text()').extract_first()), 3)
        item['ops'] = round(item['slg'] + item['obp'], 3)
        return item
