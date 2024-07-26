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
url = 'https://sports.news.naver.com/kbaseball/record/index.nhn?category=kbo&year=2024'  # 실제 데이터 소스 URL로 수정 필요
baseballData = urllib.request.urlopen(url)
source = baseballData.read()
baseballData.close()

# HTML 파싱
soup = BeautifulSoup(source, 'html.parser')
scripts = soup.find_all('script')

# JSON 데이터 찾기
recordJsonData = None
for script in scripts:
    line = str(script)
    if 'var ' in line and 'jsonTeamRecord' in line:
        recordList = line.split('jsonTeamRecord = ')
        if len(recordList) > 1:
            record = recordList[1].split('};')[0] + '}'
            recordJsonData = record.strip()

# JSON 파싱
if recordJsonData:
    r = json.loads(recordJsonData)
    regularTeamRecordList = r['regularTeamRecordList']

    # HTML 테이블 생성
    html_output = '''
    <table border="1">
        <tr>
            <th>순위</th>
            <th>팀명</th>
            <th>경기수</th>
            <th>승</th>
            <th>패</th>
            <th>무</th>
            <th>승률</th>
            <th>게임차</th>
            <th>최근 10경기</th>
        </tr>
    '''

    order = 0
    for team in regularTeamRecordList:
        order += 1
        tn = preformat_cjk(team['teamName'], 10)
        gameCount = team['gameCount']
        won = team['won']
        lost = team['lost']
        drawn = team['drawn']
        wra = format(float(team['wra']), '.3f')  # Format winning percentage to 3 decimal places
        winDiff = team['winDiff']
        recentResult = team['recentResult']

        # 팀명이 '두산'인지 확인하고 스타일 변경
        row_class = 'blue-row' if '두산' in team['teamName'] else ''
        
        html_output += '''
        <tr class="{}">
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
        '''.format(row_class, order, tn, gameCount, won, lost, drawn, wra, winDiff, recentResult)

    html_output += '</table>'
    
    # HTML 파일로 저장
    with open('./rank/baseball_records.html', 'w', encoding='utf-8') as f:
        f.write('''
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>두산베어스</title>
            <meta property="og:type" content="website">
            <meta property="og:title" content="페이지 제목">
            <meta property="og:description" content="페이지 설명">
            <meta property="og:image" content="http://www.mysite.com/article/article1_featured_image.jpg">
            <meta property="og:url" content="http://www.mysite.com/article/article1.html">
            <meta name="twitter:card" content="summary">
            <meta name="twitter:title" content="페이지 제목">
            <meta name="twitter:description" content="페이지 설명">
            <meta name="twitter:image" content="http://www.mysite.com/article/article1.html">
            <meta name="twitter:domain" content="사이트 명">
            <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-gov.min.css">
            <!-- icons -->
            <link href="https://fonts.googleapis.com/css?family=Material+Icons|Material+Icons+Outlined|Material+Icons+Round" rel="stylesheet">
            <!-- symbols -->
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@NaN,0,0,0">
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
            <link rel="stylesheet" href="https://maxst.icons8.com/vue-static/landings/line-awesome/line-awesome/1.3.0/css/line-awesome.min.css">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css">
            <link rel="stylesheet" href="./resources/css/styles.css">
        </head>
        <body>
            <div id="wrap">
                <!-- skip 네비게이션 -->
                <div id="skip-nav">
                    <a href="#gnb">전체 메뉴 바로가기</a>
                    <a href="#container">본문 바로가기</a>
                </div>
                <!-- 헤더 영역 -->
                <div id="header-top">
                    <div class="inner">공지사항</div>
                </div>
                <header id="header">
                    <div class="inner">
                        <div class="head-in">
                            <h1 id="logo">
                                <a href="#">두산베어스</a>
                            </h1>
                            <nav id="gnb">
                                <dl>
                                    <dt><a href="#">구단소개</a></dt>
                                </dl>
                                <dl>
                                    <dt><a href="#">선수소개</a></dt>
                                </dl>
                                <dl>
                                    <dt><a href="#">기록실</a></dt>
                                </dl>
                                <dl>
                                    <dt><a href="#">역대감독</a></dt>
                                </dl>
                            </nav>
                            <div class="util">
                                <button class="btn-nav sch">통합검색</button>
                                <a href="#" class="btn-nav login">로그인</a>
                                <a href="#" class="btn-nav join">회원가입</a>
                                <a href="#" class="btn-nav my">마이페이지</a>
                                <button class="btn-nav all">전체메뉴</button>
                            </div>
                        </div>
                    </div>
                </header>
                <!-- slide -->
                <div class="swiper slide-intro">
                    <div class="swiper-wrapper">
                        <div class="swiper-slide">
                            <picture>
                                <source srcset="https://www.doosanbears.com/_next/image?url=https%3A%2F%2Fd3uesnxiude69b.cloudfront.net%2Fimgbbs%2F202405%2Fb22f47fb-5864-42b7-ab2e-febd5c585e93.jpg&w=1920&q=75" media="(min-width: 1024px)">
                                <source srcset="https://www.doosanbears.com/_next/image?url=https%3A%2F%2Fd3uesnxiude69b.cloudfront.net%2Fimgbbs%2F202405%2Ff790d776-72e3-4ad0-8b9a-b801195b5362.JPG&w=1920&q=75" media="(min-width: 600px)">
                                <source srcset="https://www.doosanbears.com/_next/image?url=https%3A%2F%2Fd3uesnxiude69b.cloudfront.net%2Fimgbbs%2F202407%2F6588b82a-24cf-4d8c-8378-1dbe54e36e81.JPG&w=1920&q=75">
                                <img src="https://www.doosanbears.com/_next/image?url=https%3A%2F%2Fd3uesnxiude69b.cloudfront.net%2Fimgbbs%2F202407%2F6588b82a-24cf-4d8c-8378-1dbe54e36e81.JPG&w=1920&q=75" alt="slide-intro">
                            </picture>
                        </div>
                    </div>
                </div>
                <!-- main -->
                <div id="main">
                    <div id="content" class="pb50">
                        <section class="section" id="ranking-section">
                            <div class="inner">
                                <h2 class="title">현재 랭킹</h2>
                                ''' + html_output + '''
                            </div>
                        </section>
                    </div>
                </div>
                <!-- 푸터 -->
                <footer id="footer">
                    <div class="inner">
                        <div class="foot-in">
                            <ul class="policy">
                                <li><a href="#">개인정보 처리방침</a></li>
                                <li><a href="#">이용약관</a></li>
                                <li><a href="#">윤리경영</a></li>
                            </ul>
                            <div class="copyright">
                                <p>&copy; 두산베어스. All Rights Reserved.</p>
                            </div>
                        </div>
                    </div>
                </footer>
            </div>
        </body>
        </html>
        ''')

print("HTML 파일이 생성되었습니다.")
