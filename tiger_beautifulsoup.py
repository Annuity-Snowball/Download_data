# 타이거는 beautifulsoup 안됨... none 값으로 넘어옴
import requests

from bs4 import BeautifulSoup

#웹페이지 가져오기

res = requests.get('https://www.tigeretf.com/ko/reference/list.do')

#웹페이지 파싱하기

soup = BeautifulSoup(res.content,'html.parser')

#필요한 데이터 추출하기

items = soup.select_one('#listArea > tr:nth-child(3) > td:nth-child(1) > div')

#추출한 데이터 활용하기(밑에 코드는 예시로, 실제와 다를 수 있다)
print(items)