# BASEBALL CLI
日本プロ野球の試合結果、順位表、個人成績を確認できるコマンドラインツール（CLI）です。

データは NPB 公式サイトからスクレイピングして取得しています。（負荷をかけないよう6時間以内はキャッシュを利用します）

~~[NPB BIP](https://npb.jp/services/npbbip/) 個人使用させてくれませんかね。~~


# Install

```bash
# ソースからビルド
$ git clone https://github.com/buenaV1sta/baseball-cli
$ cd baseball-cli
$ python3 setup.py sdist
$ sudo pip3 install dist/baseball-cli-0.0.1.tar.gz
```

```bash
# TODO: PyPI 登録後であれば
$ pip3 install baseball-cli
```

# Usage

## Get baseball match result

```bash
# 昨日の試合結果
$ npb results

# ジャイアンツの今年の試合結果一覧
$ npb results --team g

# ジャイアンツの2019年の試合結果一覧
$ npb results --year 2019 --team g

# 2019年4月10日の試合結果
$ npb results --year 2019 --month 4 --day 10
```

### command options
- --year (int)
  - 年 (2005~今年)
- --month (int)
  - 月 (3~11)
- --day (int)
  - 日 (1~31)
- --team (string)
  - チームコード（Explain options 参照）

## Get standings

```bash
# 今年のパ・リーグの順位表
$ npb standings

# 今年のパ・リーグの順位表
$ npb standings --league p

# 今年のセ・リーグの順位表
$ npb standings --league c

# 2019年のセ・リーグの順位表
$ npb standings --league c --year 2019

# 2019年のセ・リーグの順位表を1行で表示
$ npb standings --league c --year 2019 --one-line
```

### command options
- --year (int)
  - 年 (2005~今年)
- --league (string)
  - リーグコード（Explain options 参照）
- --one-line (bool)
  - 1行で表示するオプション


## Get pitching stats

```bash
# 今年の両リーグの規定投球回以上の先発、セーブ上位、HP 上位
$ npb pstats

# 今年のセ・リーグの規定投球回以上の先発、セーブ上位、HP 上位（--sort 省略時は「投球回」降順）
$ npb pstats --league c

# 今年のセ・リーグの規定投球回以上の先発、セーブ上位、HP 上位を「奪三振」の降順で表示
$ npb pstats --league c --sort so

# 今年のセ・リーグの規定投球回以上の先発、セーブ上位、HP 上位を「防御率」の昇順で表示
$ npb pstats --league c --sort era --asc

# 今年のパ・リーグの規定投球回以上の先発、セーブ上位、HP 上位
$ npb pstats --league p

# 2019年のパ・リーグの規定投球回以上の先発、セーブ上位、HP 上位
$ npb pstats --league p --year 2019

# 今年のジャイアンツの登板数1以上の投手の投球成績表示
$ npb pstats --team g

# 2019年のジャイアンツの登板数1以上の投手の投球成績表示
$ npb bstats --team g --year 2019

# ジャイアンツ時代の杉内投手の成績（2005年以降）表示
$ npb pstats --team g --name 杉内

# 杉内投手の通算成績（2005年以降）表示
$ npb pstats --name 杉内
```

### command options
- --year (int)
  - 年 (2005~今年)
- --league (string)
  - リーグコード（Explain options 参照）
- --team (string)
  - チームコード（Explain options 参照）
- --name (string)
  - 選手名
- --sort (string))
  - ソートする対象（Explain options 参照）
- --asc (bool)
  - 昇順ソート

## Get batting stats

```bash
# 今年の両リーグの規定打席到達者
$ npb bstats

# 今年のセ・リーグの規定打席到達者（--sort 省略時は「OPS」降順）
$ npb bstats --league c

# 今年のセ・リーグの規定打席到達者を「ホームラン数」の降順で表示
$ npb bstats --league c --sort hr

# 今年のセ・リーグの規定打席到達者を「三振」の昇順で表示
$ npb bstats --league c --sort so --asc

# 今年のパ・リーグの規定打席到達者
$ npb bstats --league p

# 2019年のパ・リーグの規定打席到達者
$ npb bstats --league p --year 2019

# 今年のジャイアンツの登板数1以上の投手または打席数1以上の打者の打撃成績表示
$ npb bstats --team g

# 2019年のジャイアンツの登板数1以上の投手または打席数1以上の打者の打撃成績表示
$ npb bstats --team g --year 2019

# ホークス時代の内川選手の成績（2005年以降）表示
$ npb bstats --team h --name 内川

# 内川選手の通算成績（2005年以降）表示
$ npb bstats --name 内川
```

### command options
- --year (int)
  - 年 (2005~今年)
- --league (string)
  - リーグコード（Explain options 参照）
- --team (string)
  - チームコード（Explain options 参照）
- --name (string)
  - 選手名
- --sort (string))
  - ソートする対象（Explain options 参照）
- --asc (bool)
  - 昇順ソート


# Explain options

オプションの補足です。

## `--team` で設定できる値
```
l: 埼玉西武ライオンズ
h: 福岡ソフトバンクホークス
e: 東北楽天ゴールデンイーグルス
m: 千葉ロッテマリーンズ
f: 北海道日本ハムファイターズ
bs: オリックス・バファローズ
g: 読売ジャイアンツ
db: 横浜DeNAベイスターズ
yb: 横浜ベイスターズ (2005~2011)
t: 阪神タイガース
c: 広島東洋カープ
d: 中日ドラゴンズ
s: 東京ヤクルトスワローズ
```

## `--league` で設定できる値
```
p: パ・リーグ
c: セ・リーグ
```

## pstats コマンドの `--sort` で設定できる値
```
year: シーズン
team: チーム名
name: 選手名
games: 登板数
win: 勝
lose: 敗
save: セーブ
hold: ホールド
hp: ホールドポイント
cg: 完投
sho: 完封
non_bb: 無四球
w_per: 勝率
bf: 対戦打者数
ip: 投球回（デフォルトでは投球回でソートします）
h: 被安打
hr: 被本塁打
bb: 与四球
ibb: 敬遠
hbp: 与死球
so: 奪三振
wp: ワイルドピッチ
bk: ボーク
r: 失点
er: 自責点
era: 防御率
kbb: K/BB
whip: WHIP
```

## bstats コマンドの `--sort` で設定できる値
```
year: シーズン
team: チーム名
name: 選手名
games: 試合数
pa: 打席数
ab: 打数
run: 得点
hit: 安打
double: 二塁打
triple: 三塁打
hr: 本塁打
tb: 塁打
rbi: 打点
sb: 盗塁
cs: 盗塁死
sbp: 盗塁成功率
sh: 犠打
sf: 犠飛
bb: 四球
ibb: 敬遠
hbp: 死球
so: 三振
dp: ダブルプレー
ba: 打率
slg: 長打率
obp: 出塁率
ops: OPS（デフォルトでは OPS でソートします）
```

# Test
```bash
$ cd baseball-cli
$ pytest
```

# Scraping from

[NPB公式](https://npb.jp)
