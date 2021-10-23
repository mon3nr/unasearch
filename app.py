"""
釣り掲示板から、関東ウナギ釣りに関する記事を抽出して、CSVに変換する

http://hazebbs.com/f/index.html
"""

import requests
import sys
from datetime import datetime
from dateutil.parser import parse
from bs4 import BeautifulSoup
import re

"""
CSV ヘッダー
"""
columns = ('title', 'name', 'year', 'month', 'userid', 'content', 'point')

"""
記事抽出する掲示板URL
"""
bbslists = {
    '関東ウナギ釣り': 'http://hazebbs.com/bbs3/unagi/html/log/1211857869.html',
    '関東ウナギ釣り(その2)': 'http://hazebbs.com/bbs3/unagi/html/log/1279840340.html',
    '関東ウナギ釣り(その3)': 'http://hazebbs.com/bbs3/test2/mread.cgi/unagi/1408241467/49-98',
    '東京のウナギ釣り場': 'http://hazebbs.com/bbs3/test/mread.cgi/unagi/1342606169/l50',
};

def extract_point(comment, headers):
    """
    記事からポイントのキーワードを抽出する。見つからない場合は etc をセット
    """
    m = re.search(
        r'(荒川|旧江戸川|江戸川|多摩川|新河岸|平和橋|新中川|旧中川|中川|平井|利根川|隅田|綾瀬|水門|河口)',
        comment)
    headers['point'] = m.groups()[0] if m else 'etc'

def extract_date(comment, headers):
    """
    記事ヘッダーの投稿時刻から、年月を抽出する
    """
    m = re.search(r'(\d+)/(\d+)/(\d+)', comment)
    if m:
        [year, month, day] = [int(i) for i in m.groups()]
        if year < 100:
            year += 2000
        headers['year'] = year
        headers['month'] = month

def parse_header(comment, headers):
    """
    HTMLから名前、投稿時刻などを抽出し、辞書に登録します
    """
    comment = comment.replace("　", " ")
    m = re.search(r'：(.+?)：(.+?)ID:(.+?)$', comment)
    if m:
        [name, posted, userid] = [i.strip() for i in m.groups()]
        extract_date(posted, headers)
        headers['name'] = name
        headers['userid'] = userid
        return True

def read_bbs(title, url, csv):
    """
    掲示板の記事を読み込み、CSV に変換します
    """
    html = requests.get(url)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text, "html.parser")
    output = soup.get_text()
    headers = dict({'title': title})
    content = ''
    for line in output.splitlines():
        if parse_header(line, headers):
            headers['content'] = content
            extract_point(content, headers)
            line = list()
            for column in columns:
                value = headers[column]
                line.append('"' + str(value) + '"')
            csv.append(','.join(line))
            content = ''
        else:
            content += line.strip()

def main():
    """
    各掲示板の記事を読み込み、CSV に変換した結果を出力します
    """
    csv = list()
    for title, url in bbslists.items():
        read_bbs(title, url, csv)
    print(",".join(columns))
    print("\n".join(csv))
