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
recordJsonData = None
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
if recordJsonData:
    r = json.loads(recordJsonData[:-1])
    regularTeamRecordList = r['regularTeamRecordList']

    # HTML 테이블 생성
    html_output = '''
    <table border="1">
        <tr>
            <th>순위</th>
            <th>팀명</th>
            <th>승</th>
            <th>패</th>
            <th>무</th>
            <th>게임차</th>
            <th>최근 10경기</th>
        </tr>
    '''

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

        # 팀명이 '두산'인지 확인하고 스타일 변경
        row_class = 'blue-row' if '두산' in t['teamName'] else ''
        
        html_output += '''
        <tr class="{}">
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
        '''.format(row_class, order, tn, won, lost, drawn, winDiff, recentResult)

    html_output += '</table>'
    
    # HTML 파일로 저장
    with open('baseball_records.html', 'w', encoding='utf-8') as f:
        f.write('''
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>KBO 팀 기록</title>
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 8px;
                    text-align: center;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                /* 두산 팀의 행을 파란색으로 변경 */
                .blue-row {{
                    background-color: #b3cde0;
                }}
            </style>
        </head>
        <body>
            <h1>KBO 팀 기록</h1>
            <div id="baseball-records">
                {}
            </div>
        </body>
        </html>
        '''.format(html_output))
else:
    print('데이터를 찾을 수 없습니다.')
