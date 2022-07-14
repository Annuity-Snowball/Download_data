# 코덱스 사이트 크롤링 확인 여부 - 크롤링 가능

#라이브러리 임포트

import requests

from bs4 import BeautifulSoup

#웹페이지 가져오기

res = requests.get('http://m.kodex.com/pension.do')

#웹페이지 파싱하기

soup = BeautifulSoup(res.content,'html.parser')

#필요한 데이터 추출하기

items = soup.select('#pensionEft2 > div:nth-child(3) > table.table.mt20 > tbody > tr')

#추출한 데이터 활용하기(밑에 코드는 예시로, 실제와 다를 수 있다)
for item in items:
    print(item.select_one('td:nth-child(1) > a').get_text())