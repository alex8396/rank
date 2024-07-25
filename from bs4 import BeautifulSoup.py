import json
import unicodedata
import urllib.request
from bs4 import BeautifulSoup

def preformat_cjk(string, width, align='<', fill=' '):
    count = (width - sum(1 + (unicodedata.east_asian_width(c) in "WF") for c in string))
    return {
        '>': lambda s: fill * count + s,
        '<': lambda s: s + fill * count,
        '^': lambda s: fill * (count // 2) + s + fill * (count // 2 + count % 2)
    }[align](string)

# 데이터 가져오기
url = 'https://sports.news.naver.com/kbaseball/record/index.nhn?category=kbo&amp;year=2017'  # 실제 데이터 소스 URL로 수정 필요
baseballData = urllib.request.urlopen(url)
source = baseballData.read()
baseballData.close()

# HTML 파싱
soup = BeautifulSoup(source, 'html.parser')
soup = soup.find_all('script')

# JSON 데이터 찾기
for script in soup:
    line = str(script)
    if 'var ' in line and 'jsonTeamRecord' in line:
        recordList = line.split('jsonTeamRecord = ')

        for record in recordList:
            if record.startswith('{'):
                recordLine = record.splitlines()
                for finalLine in recordLine:
                    if finalLine.endswith('}]};'):
                        recordJsonData = finalLine

# JSON 파싱
r = json.loads(recordJsonData[:-1])
regularTeamRecordList = r['regularTeamRecordList']

# 결과 출력
order = 0
for team in regularTeamRecordList:
    t = json.loads(str(team).replace("'", '"'))
    order += 1
    tn = preformat_cjk(t['teamName'], 10)
    won = t['won']
    lost = t['lost']
    drawn = t['drawn']
    winDiff = t['winDiff']
    recentResult = t['recentResult']

    print('%02d  %s  %s  %s  %s %-5s   %s' % (order, tn, won, lost, drawn, winDiff, recentResult))
