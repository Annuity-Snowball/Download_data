# 멀티스레드로 구현
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# [2022.06.30] find_element_by_() 함수는 find_element(By., ) 과 같은 형태로 함수가 변경됨에 따른 추가 코드
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import getDatainfo
from datetime import datetime
import random

Initial_path = "C:\self_project\snowball\Download_data\pdf_files"

# 크롬 드라이버가 설치된 파일경로 설정
chromedriver = 'C:/Users/th/Desktop/webdriver/chromedriver.exe' # 윈도우

# 파일 다운로드 위치 설정을 위한 코드
chromeOptions = webdriver.ChromeOptions()  # 크롬 드라이버 옵션 설정
chromeOptions.add_argument('headless')

prefs = {"download.default_directory": Initial_path}  # 파일다운로드 경로 설정
chromeOptions.add_experimental_option("prefs", prefs)  # 옵션 정의


# 스레드 실행 함수
def crawling_selenium(product_code, product_date):
    # 접속할 사이트 설정
    driver_chrome = webdriver.Chrome(service=Service(chromedriver), options=chromeOptions)  # 설정 반영
    driver_chrome.get("http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030108")

    rand = random.randrange(3, 6)

    # 처음 사이트 들어간 후 4초 대기
    time.sleep(rand)

    # 금융상품명 검색 버튼 클릭
    search_btn = driver_chrome.find_element(By.ID, 'btnisuCd_finder_secuprodisu1_0')  # 검색 태그 선택
    search_btn.click()  # 태그 클릭
    rand2 = random.randrange(3, 6)
    time.sleep(rand2)

    # 금융상품코드를 통해서 금융상품 선택
    search_bar = driver_chrome.find_element(By.CSS_SELECTOR, '#searchText__finder_secuprodisu1_0')  # 검색 창 선택
    search_bar.clear()
    search_bar.send_keys(product_code)
    search_bar.send_keys(Keys.RETURN)
    rand3 = random.randrange(3, 6)
    time.sleep(rand3)

    # 조회날짜 선택
    elem = driver_chrome.find_element(By.ID, 'trdDd')  # 검색 태그 선택
    for _ in range(8):
        elem.send_keys(Keys.BACK_SPACE)  # clear() 를 입력하면 조회일자가 이상하게 초기화되기에 backspace로 지우는 과정 추가!
    elem.send_keys(product_date)
    elem.send_keys(Keys.RETURN)
    rand4 = random.randrange(3, 6)
    time.sleep(rand4)

    # 조회 버튼 클릭
    search_btn = driver_chrome.find_element(By.ID, 'jsSearchButton')  # 검색 태그 선택
    search_btn.click()  # 태그 클릭
    rand5 = random.randrange(3, 6)
    time.sleep(rand5)

    # 금융상품의 구성 종목 조회 - 일단 10개의 종목만 받아옴
    stock_list = list()
    stock_infos = driver_chrome.find_elements(By.CSS_SELECTOR,
                                              '#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table > tbody > tr')
    for stock_info in stock_infos:
        stock_list.append(stock_info.text.split())

    for temp_list in stock_list:
        if len(temp_list) > 6:
            temp_list[1] = " ".join(temp_list[1:-4])
            del temp_list[2:-4]
    # 드라이버 종료
    driver_chrome.quit()
    print(f"상품코드 : {product_code}, 조회날짜 : {product_date} 시작!")
    print(stock_list)
    print()

    # 파일로 저장하는 부분 후보1 - df로 하는 부분도 마지막 부분만 동작을 함 안됨
    # df = pd.DataFrame({},columns=['종목코드','구성종목명','주식수(계약수)','평가금액','시가총액','시가총액기준구성비중'])
    # for i in range(len(stock_list)):
    #     df.loc[i]=stock_list[i]
    # 파일로 저장시 lock이 필요할 듯! - 아직 동작을 안함
    # df.to_csv('C:\self_project\\acceleration_download_file\Download_data\pdf_files\\'+str(product_code)+'_'+str(product_date)+'.csv',index=False)
    # print(df)

    # 파일로 저장하는 부분 후보2
    fields = ['종목코드', '구성종목명', '주식수(계약수)', '평가금액', '시가총액', '시가총액기준구성비중']
    product_date = ''.join(product_date.split('-'))
    with open('D:\Data\pdf_files_ex\\' + str(product_code) + '_' + str(product_date) + '.csv', 'w', newline='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(stock_list)


# 실행하는 코드의 위치가 여기일 경우 실행
if __name__ == '__main__':

    df = pd.read_csv("ad.csv")
    code_list = list(df['code'])
    date_list = list(df['date'])
    payinDate_dict_bm = dict()

    for i in range(len(code_list)):
        payinDate_dict_bm[code_list[i]] = getDatainfo.getPayInDateInfo(date_list[i],
                                                                       datetime.today().strftime('%Y-%m-%d'), '0')

    product_code_list = []
    product_date_list = []
    for stock_code in payinDate_dict_bm.keys():
        for search_date in payinDate_dict_bm[stock_code]:
            product_code_list.append(stock_code)
            product_date_list.append(search_date)

    start_time = time.time()

    # with context 구문 사용
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(crawling_selenium, product_code_list[22300:], product_date_list[22300:])

    print("--- %s seconds ---" % (time.time() - start_time))