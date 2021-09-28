import mock
import pytest
from click.testing import CliRunner
from datetime import datetime
from datetime import timedelta

try:
    from baseball import main
    from baseball.utils import NpbConst
except ModuleNotFoundError:
    import sys
    sys.path.append('./')
    from baseball import main
    from baseball.utils import NpbConst


@pytest.fixture(scope='function')
def process():
    with mock.patch('npb.main.CrawlerProcess') as process:
        process.return_value = mock.Mock()
        process.crawl = mock.Mock()
        process.start = mock.Mock()
        yield process


@pytest.fixture(scope='function')
def json():
    with mock.patch('npb.main.open', mock.mock_open(), create=True) as json:
        with mock.patch('npb.main.json') as json:
            # json.return_value = mock.Mock()
            yield json


class TestCliCommand():

    def test_root(self):
        runner = CliRunner()
        result = runner.invoke(main._root)
        expected_main_help_text = 'Show results and stats and standings of '
        'Nippon Professional Baseball (NPB).'
        assert result.exit_code == 0
        assert expected_main_help_text in result.stdout

    def test_results_no_options(self, process, json):
        yesterday = datetime.today() - timedelta(days=1)
        json.load.return_value = [{
            'match1': 'dummy',
            'match2': 'dummy',
            'match3': 'dummy',
        }]
        runner = CliRunner()
        result = runner.invoke(main._root, ['results'])
        assert result.exit_code == 0
        assert datetime.strftime(yesterday, '%Y-%m-%d') in result.stdout

    def test_results_ymd(self, process, json):
        json.load.return_value = [{
            'match1': 'dummy',
            'match2': 'dummy',
            'match3': 'dummy',
        }]
        runner = CliRunner()
        result = runner.invoke(main._root, [
            'results',
            '--year', '2019',
            '--month', '4',
            '--day', '5',
            ])
        assert result.exit_code == 0
        assert '2019-04-05' in result.stdout

    def test_results_team(self, process, json):
        json.load.return_value = [
            {
                'datetime': '2019-09-05',
                'match': 'ヤ 1 - 8 広',
            },
            {
                'datetime': '2019-09-06',
                'match': 'ヤ 5 - 2 巨',
            }
        ]
        runner = CliRunner()
        result = runner.invoke(main._root, [
            'results',
            '--team', 's',
            ])
        assert result.exit_code == 0
        assert '2019-09-05: ヤ 1 - 8 広' in result.stdout
        assert '2019-09-06: ヤ 5 - 2 巨' in result.stdout

    def test_standings_no_options(self, process, json):
        json.load.return_value = [
            {
                'rank': '1',
                'team': 'dummy',
                'games': '143',
                'win': '143',
                'lose': '0',
                'draw': '0',
                'w_per': '100',
                'gb': '--',
            }
        ]
        runner = CliRunner()
        result = runner.invoke(main._root, ['standings'])
        assert result.exit_code == 0
        assert ''.join(NpbConst.STANDINGS_HEADERS) in result.stdout

    def test_standings_one_line(self, process, json):
        json.load.return_value = [
            {
                'rank': '1',
                'team': 'A',
                'games': '0',
                'win': '0',
                'lose': '0',
                'draw': '0',
                'w_per': '.000',
                'gb': '--',
            },
            {
                'rank': '2',
                'team': 'B',
                'games': '0',
                'win': '0',
                'lose': '0',
                'draw': '0',
                'w_per': '.000',
                'gb': '2.0',
            },
            {
                'rank': '3',
                'team': 'C',
                'games': '0',
                'win': '0',
                'lose': '0',
                'draw': '0',
                'w_per': '.000',
                'gb': '10.0',
            },
        ]
        runner = CliRunner()
        result = runner.invoke(main._root, ['standings', '--one-line'])
        assert result.exit_code == 0
        assert 'A----B----------------C' in result.stdout

    def test_batting_stats_no_options(self, process, json):
        json.load.return_value = [
            {
                'year': '2019',
                'team': 'dummy',
                'name': 'dummy',
            }
        ]
        runner = CliRunner()
        result = runner.invoke(main._root, ['bstats'])
        assert result.exit_code == 0
        assert ''.join(NpbConst.BATTING_STATS_HEADERS) in result.stdout

    def test_pitching_stats_no_options(self, process, json):
        json.load.return_value = [
            {
                'year': '2019',
                'team': 'dummy',
                'name': 'dummy',
            }
        ]
        runner = CliRunner()
        result = runner.invoke(main._root, ['pstats'])
        assert result.exit_code == 0
        assert ''.join(NpbConst.PITCHING_STATS_HEADERS) in result.stdout
