# -*- coding: utf-8 -*-
import datetime
import re
import os


class NpbConst:
    MAIN_HELP_TEXT = '''
        Show results and stats and standings of
         Nippon Professional Baseball (NPB).

        Team codes:

        \b
        - l: 埼玉西武ライオンズ
        - h: 福岡ソフトバンクホークス
        - e: 東北楽天ゴールデンイーグルス
        - m: 千葉ロッテマリーンズ
        - f: 北海道日本ハムファイターズ
        - bs: オリックス・バファローズ
        - g: 読売ジャイアンツ
        - db: 横浜DeNAベイスターズ
        - yb: 横浜ベイスターズ (2005~2011)
        - t: 阪神タイガース
        - c: 広島東洋カープ
        - d: 中日ドラゴンズ
        - s: 東京ヤクルトスワローズ

        League codes:

        \b
        - p: パ・リーグ
        - c: セ・リーグ
    '''
    SORT_HELP_TEXT = '''
        Pitching Sort keys:

        \b
        year:   sort by year
        team:   sort by team name
        name:   sort by player name
        games:  sort by games
        win:    sort by win
        lose:   sort by lose
        save:   sort by save
        hold:   sort by hold
        hp:     sort by hold point
        cg:     sort by complete game
        sho:    sort by shut-out
        non_bb: sort by non bb
        w_per:  sort by winning percentage
        bf:     sort by batsmen faced
        ip:     sort by innings pitched (default)
        h:      sort by hits
        hr:     sort by home runs
        bb:     sort by bases on balls
        ibb:    sort by intentional bases on balls
        hbp:    sort by hit by pitch
        so:     sort by strikeouts
        wp:     sort by wild pitches
        bk:     sort by balks
        r:      sort by unearned runs
        er:     sort by earned runs
        era:    sort by earned run average
        kbb:    sort by strikeout to walk ratio
        whip:   sort by walks plus hits per inning pitched

        Batting Sort keys:

        \b
        year:   sort by year
        team:   sort by team name
        name:   sort by player name
        games:  sort by games
        pa:     sort by plate appearances
        ab:     sort by at bats
        run:    sort by runs
        hit:    sort by hits
        double: sort by double
        triple: sort by triple
        hr:     sort by home runs
        tb:     sort by total bases
        rbi:    sort by runs batted in
        sb:     sort by stolen bases
        cs:     sort by caught stealing
        sbp:    sort by stolen bases percentage
        sh:     sort by sacrifice hits
        sf:     sort by sacrifice flies
        bb:     sort by bases on balls
        ibb:    sort by intentional bases on balls
        hbp:    sort by hit by pitch
        so:     sort by strikeouts
        dp:     sort by double plays
        ba:     sort by batting average
        slg:    sort by slugging percentage
        obp:    sort by on base percentage
        ops:    sort by on-base plus slugging (default)
    '''
    THIS_YEAR = datetime.date.today().year
    THIS_MONTH = datetime.date.today().month
    THIS_DAY = datetime.date.today().day
    TEAMS = {
        'l': 'lions',
        'h': 'hawks',
        'e': 'eagles',
        'm': 'marines',
        'f': 'fighters',
        'bs': 'buffalos',
        'g': 'giants',
        'yb': 'baystars',
        'db': 'baystars',
        't': 'tigers',
        'c': 'carp',
        'd': 'dragons',
        's': 'swallows',
    }
    TEAM_COLORS = {
        'l': ('bright_cyan', 'black'),
        'h': ('bright_yellow', 'black'),
        'e': ('red', 'black'),
        'm': ('white', 'black'),
        'f': ('black', 'white'),
        'bs': ('blue', 'black'),
        'g': ('black', 'white'),
        'yb': ('bright_blue', 'black'),
        'db': ('bright_blue', 'black'),
        't': ('bright_yellow', 'black'),
        'c': ('bright_red', 'black'),
        'd': ('cyan', 'black'),
        's': ('blue', 'black'),
    }
    ABBREVIATION_TEAMS = {
        '(西)': 'lions',
        '(ソ)': 'hawks',
        '(楽)': 'eagles',
        '(ロ)': 'marines',
        '(日)': 'fighters',
        '(オ)': 'buffalos',
        '(巨)': 'giants',
        '(デ)': 'baystars',
        '(横)': 'baystars',
        '(神)': 'tigers',
        '(広)': 'carp',
        '(中)': 'dragons',
        '(ヤ)': 'swallows',
    }
    TEAM_CODE_TO_ABBREVIATION = {
        'l': '西',
        'h': 'ソ',
        'e': '楽',
        'm': 'ロ',
        'f': '日',
        'bs': 'オ',
        'g': '巨',
        'yb': '横',
        'db': 'デ',
        't': '神',
        'c': '広',
        'd': '中',
        's': 'ヤ',
    }
    NPB_CLI_HOME = '/'.join(
        [
            os.environ['HOME'],
            '.npbcli',
        ])
    OUTPUT_JSON_FILE_PATH = '/'.join(
        [
            NPB_CLI_HOME,
            'tmp.json'
        ])
    BATTING_STATS_HEADERS = [
        "{:6}".format("YEAR"),
        "{:10}".format("TEAM"),
        "{:8}".format("GAMES"),
        "{:4}".format("PA"),
        "{:4}".format("AB"),
        "{:4}".format("R"),
        "{:4}".format("1B"),
        "{:4}".format("2B"),
        "{:4}".format("3B"),
        "{:4}".format("HR"),
        "{:4}".format("TB"),
        "{:4}".format("RBI"),
        "{:4}".format("SB"),
        "{:4}".format("CS"),
        "{:8}".format("SBP"),
        "{:4}".format("SH"),
        "{:4}".format("SF"),
        "{:4}".format("BB"),
        "{:4}".format("IBB"),
        "{:4}".format("HBP"),
        "{:4}".format("SO"),
        "{:4}".format("DP"),
        "{:8}".format("BA"),
        "{:8}".format("SLG"),
        "{:8}".format("OBP"),
        "{:8}".format("OPS"),
        "{:12}".format("PLAYER NAME"),
    ]
    PITCHING_STATS_HEADERS = [
        "{:6}".format("YEAR"),
        "{:10}".format("TEAM"),
        "{:8}".format("GAMES"),
        "{:4}".format("W"),
        "{:4}".format("L"),
        "{:4}".format("SV"),
        "{:4}".format("HLD"),
        "{:4}".format("HP"),
        "{:4}".format("CG"),
        "{:4}".format("SHO"),
        "{:6}".format("N_BB"),
        "{:8}".format("W_PER"),
        "{:6}".format("BF"),
        "{:8}".format("IP"),
        "{:4}".format("H"),
        "{:4}".format("HR"),
        "{:4}".format("BB"),
        "{:4}".format("IBB"),
        "{:4}".format("HBP"),
        "{:4}".format("SO"),
        "{:4}".format("WP"),
        "{:4}".format("BK"),
        "{:4}".format("R"),
        "{:4}".format("ER"),
        "{:6}".format("ERA"),
        "{:6}".format("K/BB"),
        "{:6}".format("WHIP"),
        "{:12}".format("PLAYER NAME"),
    ]
    STANDINGS_HEADERS = [
        "{:6}".format("RANK"),
        "{:8}".format("GAMES"),
        "{:6}".format("WIN"),
        "{:6}".format("LOSE"),
        "{:6}".format("DRAW"),
        "{:10}".format("WIN_PER"),
        "{:8}".format("GB"),
        "{:12}".format("TEAM"),
    ]
    GET_TEAM_CODE_REG_EXP = re.compile(r'/bis/teams/index_(.*).html')
    GET_MONTH_REG_EXP = re.compile(r'(.*)年度 カレンダー 【(.*)月】')
