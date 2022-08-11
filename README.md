# Download_data 사용시 주의사항
데이터로 활용할 금융상품 정보들을 다운로드 받는 코드들 입니다
- '한국 거래소 자료' 만을 다운로드해서 실제로 사용할 예정입니다(krx_selenium.py)
- vscode 활용해서 가상환경 만든 다음에 실행 할것을 권유합니다
- selenium 은 4.3.0 버전 이상을 사용해야 합니다!(4.3.0 부터 명령어가 조금 바뀌었기 때문에)
- chrome 드라이버는 103 버전을 사용해야 합니다
- 나머지 코드 실행에 필요한 라이브러리 들은 'pip install' 을 이용해서 설치를 한 후 사용을 해야 합니다
- 코드 실행시, 경로 등은 pc 맞춰서 수정을 해야 합니다

- 데이터베이스에서 값들을 입력 받을 시 db = pymysql.connect(host='localhost', port=3306, user='root', passwd='yoy0317689*', db='snowball_database', charset='utf8') 에서 passwd와 db를 본인 pc에 맞게 수정해야 합니다
- make_database_tables.py  ->  update_prices_database.py  ->  update_product_evaluate_database.py 순으로 실행을 하면 됩니다

## 라이브러리 버전
Package               Version
--------------------- ---------
async-generator       1.10
attrs                 22.1.0
certifi               2022.6.15
cffi                  1.15.1
charset-normalizer    2.1.0
colorama              0.4.5
cryptography          37.0.4
exchange-calendars    4.1.1
h11                   0.13.0
idna                  3.3
korean-lunar-calendar 0.2.1
numpy                 1.23.1
outcome               1.2.0
pandas                1.4.3
pip                   22.2.2
pycparser             2.21
pyluach               2.0.0
PyMySQL               1.0.2
pyOpenSSL             22.0.0
PySocks               1.7.1
python-dateutil       2.8.2
python-dotenv         0.20.0
pytz                  2022.1
requests              2.28.1
selenium              4.4.0
setuptools            56.0.0
six                   1.16.0
sniffio               1.2.0
sortedcontainers      2.4.0
toolz                 0.12.0
tqdm                  4.64.0
trio                  0.21.0
trio-websocket        0.9.2
urllib3               1.26.11
webdriver-manager     3.8.3
wsproto               1.1.0
