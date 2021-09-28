# -*- coding: utf-8 -*-
import scrapy
try:
    from baseball.utils import NpbConst
    from baseball.items import PitchingStatsItem
except ModuleNotFoundError:
    from utils import NpbConst
    from items import PitchingStatsItem


class PitchingStatsSpider(scrapy.Spider):
    name = 'pitching_stats'
    allowed_domains = ['npb.jp']

    def __init__(self, year, team, name, league):
        self.year = year
        self.player_name = name
        self.team_name = NpbConst.TEAMS.get(team)
        self.start_urls = []
        if self.player_name is not None and self.team_name is not None:
            for i in range(2005, year + 1):
                self.start_urls.append(
                    f'https://npb.jp/bis/{i}/stats/idp1_{team}.html'
                )
        elif self.player_name is not None and self.team_name is None:
            for i in range(2005, year + 1):
                for t in NpbConst.TEAMS.keys():
                    self.start_urls.append(
                        f'https://npb.jp/bis/{i}/stats/idp1_{t}.html'
                    )
        elif self.team_name is None:
            if league is None:
                self.start_urls = [
                    f'https://npb.jp/bis/{year}/stats/pit_c.html',
                    f'https://npb.jp/bis/{year}/stats/pit_p.html',
                ]
            else:
                self.start_urls = [
                    f'https://npb.jp/bis/{year}/stats/pit_{league}.html']
        else:
            self.start_urls = [
                f'https://npb.jp/bis/{year}/stats/idp1_{team}.html']

    def parse(self, response):
        for tr in response.xpath('//*[@id="stdivmaintbl"]/table/tr'):
            if self.team_name is not None or self.player_name is not None:
                yield self._get_personal_pitching_stats(response, tr)
            else:
                yield self._get_season_pitching_stats(response, tr)

    def _get_personal_pitching_stats(self, response, tr):
        item = PitchingStatsItem()
        if not tr.xpath('td[3]/text()').extract_first():
            return
        item['year'] = int(response.xpath(
            '/html/head/title/text()').extract_first()[0:4])
        item['name'] = tr.xpath(
            'td[2]/text()').extract_first().replace('\u3000', ' ')
        if self.player_name is not None and \
                self.player_name not in item['name']:
            return
        m = NpbConst.GET_TEAM_CODE_REG_EXP.match(response.xpath(
            '//*[@id="stdivtitle"]/h1/a[2]/@href').extract_first())
        item['team'] = NpbConst.TEAMS[m.group(1)]
        item['games'] = int(tr.xpath('td[3]/text()').extract_first())
        item['win'] = int(tr.xpath('td[4]/text()').extract_first())
        item['lose'] = int(tr.xpath('td[5]/text()').extract_first())
        item['save'] = int(tr.xpath('td[6]/text()').extract_first())
        item['hold'] = int(tr.xpath('td[7]/text()').extract_first())
        item['hp'] = int(tr.xpath('td[8]/text()').extract_first())
        item['cg'] = int(tr.xpath('td[9]/text()').extract_first())
        item['sho'] = int(tr.xpath('td[10]/text()').extract_first())
        item['non_bb'] = int(tr.xpath('td[11]/text()').extract_first())
        item['w_per'] = round(
            float(tr.xpath('td[12]/text()').extract_first()), 3)
        item['bf'] = int(tr.xpath('td[13]/text()').extract_first())
        if tr.xpath('td[15]/text()').extract_first() is not None:
            item['ip'] = float(tr.xpath(
                'td[14]/text()').extract_first() +
                tr.xpath('td[15]/text()').extract_first())
        else:
            try:
                item['ip'] = float(
                    tr.xpath('td[14]/text()').extract_first())
            except ValueError:
                item['ip'] = 0.0
        item['h'] = int(tr.xpath('td[16]/text()').extract_first())
        item['hr'] = int(tr.xpath('td[17]/text()').extract_first())
        item['bb'] = int(tr.xpath('td[18]/text()').extract_first())
        item['ibb'] = int(tr.xpath('td[19]/text()').extract_first())
        item['hbp'] = int(tr.xpath('td[20]/text()').extract_first())
        item['so'] = int(tr.xpath('td[21]/text()').extract_first())
        item['wp'] = int(tr.xpath('td[22]/text()').extract_first())
        item['bk'] = int(tr.xpath('td[23]/text()').extract_first())
        item['r'] = int(tr.xpath('td[24]/text()').extract_first())
        item['er'] = int(tr.xpath('td[25]/text()').extract_first())
        try:
            item['era'] = round(
                float(tr.xpath('td[26]/text()').extract_first()), 3)
        except ValueError:
            item['era'] = '----'
        if item['bb'] == 0:
            item['kbb'] = round(float(item['so']), 2)
        else:
            item['kbb'] = round(item['so'] / item['bb'], 2)
        if round(item['ip'] - int(item['ip']), 1) == 0.1:
            actual_ip = float(int(item['ip'])) + 0.3333333333
        elif round(item['ip'] - int(item['ip']), 1) == 0.2:
            actual_ip = float(int(item['ip'])) + 0.6666666666
        else:
            actual_ip = item['ip']
        try:
            item['whip'] = round(
                (item['h'] + item['bb']) / actual_ip,
                2)
        except ZeroDivisionError:
            item['whip'] = '----'
        return item

    def _get_season_pitching_stats(self, response, tr):
        item = PitchingStatsItem()
        if not tr.xpath('td[3]/text()').extract_first():
            return
        item['year'] = int(response.xpath(
            '/html/head/title/text()').extract_first()[0:4])
        item['team'] = self.team_name
        item['name'] = tr.xpath(
            'td[2]/text()').extract_first().replace('\u3000', ' ')
        if self.player_name is not None and \
                self.player_name not in item['name']:
            return
        item['team'] = NpbConst.ABBREVIATION_TEAMS.get(
            tr.xpath('td[3]/text()').extract_first())
        item['era'] = round(
            float(tr.xpath('td[4]/text()').extract_first()), 3)
        item['games'] = int(tr.xpath('td[5]/text()').extract_first())
        item['win'] = int(tr.xpath('td[6]/text()').extract_first())
        item['lose'] = int(tr.xpath('td[7]/text()').extract_first())
        item['save'] = int(tr.xpath('td[8]/text()').extract_first())
        item['hold'] = int(tr.xpath('td[9]/text()').extract_first())
        item['hp'] = int(tr.xpath('td[10]/text()').extract_first())
        item['cg'] = int(tr.xpath('td[11]/text()').extract_first())
        item['sho'] = int(tr.xpath('td[12]/text()').extract_first())
        item['non_bb'] = int(tr.xpath('td[13]/text()').extract_first())
        item['w_per'] = round(
            float(tr.xpath('td[14]/text()').extract_first()), 3)
        item['bf'] = int(tr.xpath('td[15]/text()').extract_first())
        if tr.xpath('td[17]/text()').extract_first() is not None:
            item['ip'] = float(tr.xpath(
                'td[16]/text()').extract_first() +
                tr.xpath('td[17]/text()').extract_first())
        else:
            item['ip'] = float(
                tr.xpath('td[16]/text()').extract_first())
        item['h'] = int(tr.xpath('td[18]/text()').extract_first())
        item['hr'] = int(tr.xpath('td[19]/text()').extract_first())
        item['bb'] = int(tr.xpath('td[20]/text()').extract_first())
        item['ibb'] = int(tr.xpath('td[21]/text()').extract_first())
        item['hbp'] = int(tr.xpath('td[22]/text()').extract_first())
        item['so'] = int(tr.xpath('td[23]/text()').extract_first())
        item['wp'] = int(tr.xpath('td[24]/text()').extract_first())
        item['bk'] = int(tr.xpath('td[25]/text()').extract_first())
        item['r'] = int(tr.xpath('td[26]/text()').extract_first())
        item['er'] = int(tr.xpath('td[27]/text()').extract_first())
        if item['bb'] == 0:
            item['kbb'] = round(float(item['so']), 2)
        else:
            item['kbb'] = round(item['so'] / item['bb'], 2)
        if round(item['ip'] - int(item['ip']), 1) == 0.1:
            actual_ip = float(int(item['ip'])) + 0.3333333333
        elif round(item['ip'] - int(item['ip']), 1) == 0.2:
            actual_ip = float(int(item['ip'])) + 0.6666666666
        else:
            actual_ip = item['ip']
        item['whip'] = round((item['h'] + item['bb']) / actual_ip, 2)
        return item
