# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BattingStatsItem(scrapy.Item):
    year = scrapy.Field()
    team = scrapy.Field()
    name = scrapy.Field()
    games = scrapy.Field()
    pa = scrapy.Field()
    ab = scrapy.Field()
    run = scrapy.Field()
    hit = scrapy.Field()
    double = scrapy.Field()
    triple = scrapy.Field()
    hr = scrapy.Field()
    tb = scrapy.Field()
    rbi = scrapy.Field()
    sb = scrapy.Field()
    cs = scrapy.Field()
    sbp = scrapy.Field()
    sh = scrapy.Field()
    sf = scrapy.Field()
    bb = scrapy.Field()
    ibb = scrapy.Field()
    hbp = scrapy.Field()
    so = scrapy.Field()
    dp = scrapy.Field()
    ba = scrapy.Field()
    slg = scrapy.Field()
    obp = scrapy.Field()
    ops = scrapy.Field()


class PitchingStatsItem(scrapy.Item):
    year = scrapy.Field()
    team = scrapy.Field()
    name = scrapy.Field()
    games = scrapy.Field()
    win = scrapy.Field()
    lose = scrapy.Field()
    save = scrapy.Field()
    hold = scrapy.Field()
    hp = scrapy.Field()
    cg = scrapy.Field()
    sho = scrapy.Field()
    non_bb = scrapy.Field()
    w_per = scrapy.Field()
    bf = scrapy.Field()
    ip = scrapy.Field()
    h = scrapy.Field()
    hr = scrapy.Field()
    bb = scrapy.Field()
    ibb = scrapy.Field()
    hbp = scrapy.Field()
    so = scrapy.Field()
    wp = scrapy.Field()
    bk = scrapy.Field()
    r = scrapy.Field()
    er = scrapy.Field()
    era = scrapy.Field()
    kbb = scrapy.Field()
    whip = scrapy.Field()


class StandingsItem(scrapy.Item):
    year = scrapy.Field()
    rank = scrapy.Field()
    team = scrapy.Field()
    games = scrapy.Field()
    win = scrapy.Field()
    lose = scrapy.Field()
    draw = scrapy.Field()
    w_per = scrapy.Field()
    gb = scrapy.Field()


class ResultsItem(scrapy.Item):
    match1 = scrapy.Field()
    match2 = scrapy.Field()
    match3 = scrapy.Field()
    match4 = scrapy.Field()
    match5 = scrapy.Field()
    match6 = scrapy.Field()


class TeamResultsItem(scrapy.Item):
    datetime = scrapy.Field()
    match = scrapy.Field()
