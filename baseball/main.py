import calendar
import click
import json
import sys
try:
    from baseball import writer
    from baseball.spiders.batting_stats import BattingStatsSpider
    from baseball.spiders.pitching_stats import PitchingStatsSpider
    from baseball.spiders.results import ResultsSpider
    from baseball.spiders.standings import StandingsSpider
    from baseball.utils import NpbConst
except ModuleNotFoundError:
    sys.path.append('./')
    from baseball import writer
    from baseball.spiders.batting_stats import BattingStatsSpider
    from baseball.spiders.pitching_stats import PitchingStatsSpider
    from baseball.spiders.results import ResultsSpider
    from baseball.spiders.standings import StandingsSpider
    from baseball.utils import NpbConst
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


def _year(func):
    for option in reversed([
        click.option(
            '--year',
            'year',
            type=click.IntRange(2005, NpbConst.THIS_YEAR),
            default=NpbConst.THIS_YEAR,
            help='Season year.'),
    ]):
        func = option(func)
    return func


def _league(func):
    for option in reversed([
        click.option(
            '--league',
            'league',
            type=click.Choice(['p', 'c']),
            help='League.'),
    ]):
        func = option(func)
    return func


def _stats_options(func):
    for option in reversed([
        click.option(
            '--team',
            'team',
            type=click.Choice(NpbConst.TEAMS.keys()),
            help='Team code.'),
        click.option(
            '--name',
            'name',
            type=str,
            help='Player name.'),
        click.option(
            '--sort',
            'sort',
            type=str,
            help=NpbConst.SORT_HELP_TEXT),
        click.option(
            '--asc',
            'asc',
            is_flag=True,
            help='Sort in ascending order.'),
    ]):
        func = option(func)
    return func


def _results_options(func):
    for option in reversed([
        click.option(
            '--month',
            'month',
            type=click.IntRange(3, 11),
            default=NpbConst.THIS_MONTH,
            help='Month.'),
        click.option(
            '--day',
            'day',
            type=click.IntRange(1, 31),
            default=NpbConst.THIS_DAY - 1,
            help='Day.'),
        click.option(
            '--team',
            'team',
            type=click.Choice(NpbConst.TEAMS.keys()),
            help='Team code.')
    ]):
        func = option(func)
    return func


def _standings_options(func):
    for option in reversed([
        click.option(
            '--one-line',
            'one_line',
            is_flag=True,
            help='Shows standings one line.'),
    ]):
        func = option(func)
    return func


@click.group(
    invoke_without_command=True,
    no_args_is_help=True,
    help=NpbConst.MAIN_HELP_TEXT)
def _root():
    pass


@_root.command(help='Shows stats of pitcher.')
@_year
@_league
@_stats_options
def pstats(year, team, name, league, sort, asc):
    configure_logging(install_root_handler=False)
    process = CrawlerProcess(get_project_settings())
    process.crawl(
        PitchingStatsSpider,
        year=year,
        team=team,
        name=name,
        league=league)
    process.start()
    with open(NpbConst.OUTPUT_JSON_FILE_PATH) as f:
        data = json.load(f)
    writer.show_pitching_stats(data, year, team, name, league, sort, asc)


@_root.command(help='Shows stats of batter.')
@_year
@_league
@_stats_options
def bstats(year, team, name, league, sort, asc):
    configure_logging(install_root_handler=False)
    process = CrawlerProcess(get_project_settings())
    process.crawl(
        BattingStatsSpider,
        year=year,
        team=team,
        name=name,
        league=league)
    process.start()
    with open(NpbConst.OUTPUT_JSON_FILE_PATH) as f:
        data = json.load(f)
    writer.show_batting_stats(data, year, team, name, league, sort, asc)


@_root.command(help='Shows standings.')
@_year
@_league
@_standings_options
def standings(year, league, one_line):
    configure_logging(install_root_handler=False)
    process = CrawlerProcess(get_project_settings())
    process.crawl(StandingsSpider, year=year, league=league)
    process.start()
    with open(NpbConst.OUTPUT_JSON_FILE_PATH) as f:
        data = json.load(f)
    if one_line is True:
        writer.show_standings_one_line(data)
    else:
        writer.show_standings(data, league)


@_root.command(help='Shows game result.')
@_year
@_results_options
def results(year, month, day, team):
    if day == 0:
        month -= 1
        _, day = calendar.monthrange(year, month)
    configure_logging(install_root_handler=False)
    process = CrawlerProcess(get_project_settings())
    process.crawl(ResultsSpider, year=year, month=month, day=day, team=team)
    process.start()
    with open(NpbConst.OUTPUT_JSON_FILE_PATH) as f:
        data = json.load(f)
    if len(data) == 0:
        click.secho('No data.', fg='red')
        return
    if team is not None:
        writer.show_team_results(data, team)
    else:
        index = 0
        if len(data) == 2:
            if month != 3:
                index = 1
        writer.show_results(data, index, year, month, day)


def main():
    try:
        _root()
    except Exception as e:
        raise e
        # click.echo(e, err=True)
        # sys.exit(1)


if __name__ == '__main__':
    main()
