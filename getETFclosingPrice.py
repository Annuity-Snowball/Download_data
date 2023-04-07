from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# [2022.06.30] find_element_by_() 함수는 find_element(By., ) 과 같은 형태로 함수가 변경됨에 따른 추가 코드
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import shutil
import getDatainfo
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import csv
import threading
import random

# 필독!!!!!!!!!!!
# 여기에 '파일을 저장할 폴더의 경로' 수정!!!
Initial_path = "C:\\Users\pth99\OneDrive\Desktop\ETF_closing"

# # 필독!!!!!!!!!!!
# # 크롬 드라이버가 설치된 파일경로 설정
chromedriver = 'C:\\Users\pth99\OneDrive\Desktop\\chromedriver.exe'  # 윈도우

# 파일 다운로드 위치 설정을 위한 코드
chromeOptions = webdriver.ChromeOptions()  # 크롬 드라이버 옵션 설정
prefs = {"download.default_directory": Initial_path}  # 파일다운로드 경로 설정
chromeOptions.add_experimental_option("prefs", prefs)  # 옵션 정의

def crawling_selenium(product_date):
    driver_chrome = webdriver.Chrome(service=Service(chromedriver), options=chromeOptions)  # 설정 반영
    driver_chrome.get("http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030201")

    # 랜덤으로 sleep
    rand = random.randrange(3, 6)
    time.sleep(rand)

    # 조회날짜 선택
    elem = driver_chrome.find_element(By.ID, 'trdDd')  # 검색 태그 선택
    for _ in range(8):
        elem.send_keys(Keys.BACK_SPACE)  # clear() 를 입력하면 조회일자가 이상하게 초기화되기에 backspace로 지우는 과정 추가!
    elem.send_keys(product_date)
    elem.send_keys(Keys.RETURN)
    # 랜덤으로 sleep
    rand = random.randrange(3, 6)
    time.sleep(rand)

    # 조회 버튼 클릭
    search_btn = driver_chrome.find_element(By.ID, 'jsSearchButton')  # 검색 태그 선택
    search_btn.click()  # 태그 클릭
    # 랜덤으로 sleep
    rand = random.randrange(3, 6)
    time.sleep(rand)

    # 조회 버튼 클릭
    search_btn = driver_chrome.find_element(By.ID, 'jsSearchButton')  # 검색 태그 선택
    search_btn.click()  # 태그 클릭
    # 랜덤으로 sleep
    rand = random.randrange(3, 6)
    time.sleep(rand)

    # 다운로드 버튼 클릭
    search_btn = driver_chrome.find_element(By.CLASS_NAME, 'CI-MDI-UNIT-DOWNLOAD')  # 검색 태그 선택
    search_btn.click()  # 태그 클릭
    # 랜덤으로 sleep
    rand = random.randrange(3, 6)
    time.sleep(rand)

    product_date = ''.join(product_date.split('-'))

    # csv 파일 다운로드 클릭
    _lock.acquire()  # 락 키 얻음 - 동기화 이슈로 인해서 lock 필요
    search_btn = driver_chrome.find_elements(By.CLASS_NAME, 'ico_filedown')  # 검색 태그 선택
    search_btn[1].click()  # 태그 클릭
    time.sleep(2)
    # 파일명 수정
    filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)], key=os.path.getctime)
    shutil.move(filename, os.path.join(Initial_path, "ETF_" + product_date + ".csv"))
    time.sleep(1)
    # 드라이버 종료
    driver_chrome.quit()

    _lock.release()  # 락 키 반환 - 동기화 이슈로 인해서 lock 필요


if __name__ == '__main__':
    date_list = getDatainfo.getDailyDateInfo('2015-01-01', datetime.today().strftime('%Y-%m-%d')) # ETF 종가 파일 다운받을 날짜 리스트 생성
    print('after create date list')

    _lock = threading.Lock()

    # 필독!!!!
    # max_workers의 개수는 컴퓨터 사양에 맞게 수정하면 됨!! 10개정도로 하면 될듯?
    # max_workers의 개수가 많을 수록 동시에 띄우는 창이 많아짐!
    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(crawling_selenium, date_list)
