# lock을 구현해야 할 듯, 다운로드가 그때그때 다르게 다운이 됨.... ㅠㅠ

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

Initial_path="C:\self_project\snowball\Download_data\pdf_files"


# 크롬 드라이버가 설치된 파일경로 설정
chromedriver = 'C:/Users/LG/dev_python/Webdriver/chromedriver.exe' # 윈도우 

# 파일 다운로드 위치 설정을 위한 코드
chromeOptions = webdriver.ChromeOptions() # 크롬 드라이버 옵션 설정
prefs = {"download.default_directory" : Initial_path} # 파일다운로드 경로 설정
chromeOptions.add_experimental_option("prefs",prefs) # 옵션 정의

def crawling_selenium(product_code,product_date):
    driver_chrome = webdriver.Chrome(service=Service(chromedriver), options=chromeOptions)  # 설정 반영
    driver_chrome.get("http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030108")



    # 처음 사이트 들어간 후 4초 대기
    time.sleep(3)


    # 금융상품명 검색 버튼 클릭
    search_btn = driver_chrome.find_element(By.ID, 'btnisuCd_finder_secuprodisu1_0') # 검색 태그 선택
    search_btn.click() # 태그 클릭
    time.sleep(3)

    # 금융상품코드를 통해서 금융상품 선택
    search_bar = driver_chrome.find_element(By.CSS_SELECTOR,'#searchText__finder_secuprodisu1_0') # 검색 창 선택
    search_bar.clear()
    search_bar.send_keys(product_code)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(3)
    

    # 조회날짜 선택 
    elem = driver_chrome.find_element(By.ID, 'trdDd') # 검색 태그 선택
    for _ in range(8):
        elem.send_keys(Keys.BACK_SPACE) # clear() 를 입력하면 조회일자가 이상하게 초기화되기에 backspace로 지우는 과정 추가!
    elem.send_keys(product_date)
    elem.send_keys(Keys.RETURN)
    time.sleep(3)


    # 조회 버튼 클릭
    search_btn = driver_chrome.find_element(By.ID, 'jsSearchButton') # 검색 태그 선택
    search_btn.click() # 태그 클릭
    time.sleep(3)


    # 조회 버튼 클릭
    search_btn = driver_chrome.find_element(By.ID, 'jsSearchButton') # 검색 태그 선택
    search_btn.click() # 태그 클릭
    time.sleep(3)

    # 다운로드 버튼 클릭
    search_btn = driver_chrome.find_element(By.CLASS_NAME, 'CI-MDI-UNIT-DOWNLOAD') # 검색 태그 선택
    search_btn.click() # 태그 클릭
    time.sleep(3)


    product_date = ''.join(product_date.split('-'))
    
    # csv 파일 다운로드 클릭
    _lock.acquire() # 락 키 얻음 - 동기화 이슈로 인해서 lock 필요
    search_btn = driver_chrome.find_elements(By.CLASS_NAME, 'ico_filedown') # 검색 태그 선택
    search_btn[1].click() # 태그 클릭
    time.sleep(2)
    # 파일명 수정
    filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
    shutil.move(filename,os.path.join(Initial_path,str(product_code)+"_"+product_date+".csv"))   
    _lock.release() # 락 키 반환 - 동기화 이슈로 인해서 lock 필요

    


                
    # 드라이버 종료     
    driver_chrome.quit()

if __name__ == '__main__':
    
    df = pd.read_csv("C:\self_project\snowball\Download_data\\ad.csv")
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
            
            
    _lock = threading.Lock()
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(crawling_selenium, product_code_list[:10], product_date_list[:10])
