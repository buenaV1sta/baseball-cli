import click
from baseball.utils import NpbConst


def show_standings_one_line(data):
    output = []
    gb = 0
    for t in data:
        try:
            wgb = float(t.get('gb')) - gb
            gb = float(t.get('gb'))
        except ValueError:
            output.append(t.get('team')[0])
            continue
        line = '-' * int(wgb / 0.5)
        output.append(line)
        output.append(t.get('team')[0])
    click.secho(''.join(output))


def show_standings(data, league):
    color = 'green' if league == 'c' else 'cyan'
    click.secho(''.join(NpbConst.STANDINGS_HEADERS), bg=color, fg='black')
    for t in data:
        body = [
            "{:6}".format(str(t.get('rank'))),
            "{:8}".format(str(t.get('games'))),
            "{:6}".format(str(t.get('win'))),
            "{:6}".format(str(t.get('lose'))),
            "{:6}".format(str(t.get('draw'))),
            "{:10}".format(str(t.get('w_per'))),
            "{:8}".format(str(t.get('gb'))),
            "{:12}".format(t.get('team')),
        ]
        click.secho(''.join(body))


def show_team_results(data, team):
    data.sort(key=lambda x: x.get('datetime'))
    for t in data:
        import re
        regex = re.compile(r'(.*) ([0-9\*]+) - ([0-9\*]+) (.*)')
        m = regex.match(t.get('match'))
        home_team = m.group(1)
        away_team = m.group(4)
        home_score = m.group(2)
        away_score = m.group(3)
        abbreviation = NpbConst.TEAM_CODE_TO_ABBREVIATION.get(team)
        color = 'green'
        if abbreviation == home_team:
            my_score = home_score
            enemy_score = away_score
        elif abbreviation == away_team:
            my_score = away_score
            enemy_score = home_score
        if my_score == '*':
            color = 'cyan'
        elif my_score == enemy_score:
            color = 'yellow'
        elif int(my_score) > int(enemy_score):
            color = 'red'
        else:
            color = 'blue'
        click.secho(''.join([
            t.get('datetime'),
            ': ',
            t.get('match'),
        ]), fg=color)


def show_results(data, index, year, month, day):
    click.secho('-'.join([
        str(year),
        '{:0>2}'.format(str(month)),
        '{:0>2}'.format(str(day))
    ]), fg='red')
    for i in range(1, 7):
        result = data[index].get(f'match{i}')
        if not any(data[index].values()):
            click.secho('No data.', fg='red')
            return
        if result is not None:
            click.secho(result)


def show_pitching_stats(data, year, team, name, league, sort, asc):
    if len(data) == 0:
        click.secho('No data.', fg='red')
    else:
        bg, fg = NpbConst.TEAM_COLORS.get(team) or ('bright_green', 'black')
        click.secho(''.join(NpbConst.PITCHING_STATS_HEADERS),
                    bg=bg, fg=fg)
    seen = []
    data = [x for x in data if x not in seen and not seen.append(x)]
    data.sort(key=lambda x: x.get(
        sort if sort is not None else 'ip', x.get('ip')), reverse=not asc)
    for t in data:
        body = [
            "{:6}".format(str(t.get('year'))),
            "{:10}".format(t.get('team')),
            "{:8}".format(str(t.get('games'))),
            "{:4}".format(str(t.get('win'))),
            "{:4}".format(str(t.get('lose'))),
            "{:4}".format(str(t.get('save'))),
            "{:4}".format(str(t.get('hold'))),
            "{:4}".format(str(t.get('hp'))),
            "{:4}".format(str(t.get('cg'))),
            "{:4}".format(str(t.get('sho'))),
            "{:6}".format(str(t.get('non_bb'))),
            "{:8}".format("{:0<5}".format(str(t.get('w_per')))),
            "{:6}".format(str(t.get('bf'))),
            "{:8}".format(str(t.get('ip'))),
            "{:4}".format(str(t.get('h'))),
            "{:4}".format(str(t.get('hr'))),
            "{:4}".format(str(t.get('bb'))),
            "{:4}".format(str(t.get('ibb'))),
            "{:4}".format(str(t.get('hbp'))),
            "{:4}".format(str(t.get('so'))),
            "{:4}".format(str(t.get('wp'))),
            "{:4}".format(str(t.get('bk'))),
            "{:4}".format(str(t.get('r'))),
            "{:4}".format(str(t.get('er'))),
            "{:6}".format("{:0<4}".format(str(t.get('era')))),
            "{:6}".format("{:0<4}".format(str(t.get('kbb')))),
            "{:6}".format("{:0<4}".format(str(t.get('whip')))),
            "{:8}".format(t.get('name')),
        ]
        click.secho(''.join(body))


def show_batting_stats(data, year, team, name, league, sort, asc):
    if len(data) == 0:
        click.secho('No data.', fg='red')
    else:
        bg, fg = NpbConst.TEAM_COLORS.get(team) or ('bright_green', 'black')
        click.secho(''.join(NpbConst.BATTING_STATS_HEADERS),
                    bg=bg, fg=fg)
    data.sort(key=lambda x: x.get(
        sort if sort is not None else 'ops', x.get('ops')), reverse=not asc)
    for t in data:
        body = [
            "{:6}".format(str(t.get('year'))),
            "{:10}".format(t.get('team')),
            "{:8}".format(str(t.get('games'))),
            "{:4}".format(str(t.get('pa'))),
            "{:4}".format(str(t.get('ab'))),
            "{:4}".format(str(t.get('run'))),
            "{:4}".format(str(t.get('hit'))),
            "{:4}".format(str(t.get('double'))),
            "{:4}".format(str(t.get('triple'))),
            "{:4}".format(str(t.get('hr'))),
            "{:4}".format(str(t.get('tb'))),
            "{:4}".format(str(t.get('rbi'))),
            "{:4}".format(str(t.get('sb'))),
            "{:4}".format(str(t.get('cs'))),
            "{:8}".format("{:0<5}".format(str(t.get('sbp')))),
            "{:4}".format(str(t.get('sh'))),
            "{:4}".format(str(t.get('sf'))),
            "{:4}".format(str(t.get('bb'))),
            "{:4}".format(str(t.get('ibb'))),
            "{:4}".format(str(t.get('hbp'))),
            "{:4}".format(str(t.get('so'))),
            "{:4}".format(str(t.get('dp'))),
            "{:8}".format("{:0<5}".format(str(t.get('ba')))),
            "{:8}".format("{:0<5}".format(str(t.get('slg')))),
            "{:8}".format("{:0<5}".format(str(t.get('obp')))),
            "{:8}".format("{:0<5}".format(str(t.get('ops')))),
            "{:8}".format(t.get('name')),
        ]
        click.secho(''.join(body))
