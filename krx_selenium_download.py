from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# [2022.06.30] find_element_by_() 함수는 find_element(By., ) 과 같은 형태로 함수가 변경됨에 따른 추가 코드
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import shutil

Initial_path="C:\self_project\\acceleration_download_file\Download_data\pdf_files"


# 크롬 드라이버가 설치된 파일경로 설정
chromedriver = 'C:/Users/LG/dev_python/Webdriver/chromedriver.exe' # 윈도우 

# 파일 다운로드 위치 설정을 위한 코드
chromeOptions = webdriver.ChromeOptions() # 크롬 드라이버 옵션 설정
prefs = {"download.default_directory" : Initial_path} # 파일다운로드 경로 설정
chromeOptions.add_experimental_option("prefs",prefs) # 옵션 정의
driver_chrome = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions) # 설정 반영

def crawling_selenium(product_date):
    # 접속할 사이트 설정
    driver_chrome.get("http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030108")



    # 처음 사이트 들어간 후 4초 대기
    time.sleep(4)


    # 종목명 검색 클릭
    search_btn = driver_chrome.find_element(By.ID, 'btnisuCd_finder_secuprodisu1_0') # 검색 태그 선택
    search_btn.click() # 태그 클릭
    time.sleep(4)

    # 종목코드 및 종목명 선택
    search_btn = driver_chrome.find_element(By.CSS_SELECTOR,'#jsGrid__finder_secuprodisu1_0 > tbody > tr:nth-child(2)') # 검색 태그 선택
    # 종목코드 받아오기
    product_code = search_btn.find_element(By.CSS_SELECTOR,'td').text
    search_btn.click() # 태그 클릭
    time.sleep(4)

    print("-------------------------------------------")
    print(product_code)
    print("-------------------------------------------")
    time.sleep(2)

    # 조회날짜 선택1
    # 조회일자 클릭
    '''
    search_btn = driver_chrome.find_element(By.CLASS_NAME, 'cal-btn-open') # 검색 태그 선택
    search_btn.click() # 태그 클릭
    time.sleep(4)

    # 조회일 클릭 - 마지막의 tr은 몇주차, td는 요일
    search_btn = driver_chrome.find_element(By.CSS_SELECTOR,'#MDCSTAT050_FORM > div.search_tb > div > table > tbody > tr:nth-child(2) > td > div > div > div > div.cal-box.cal-monthly > div.cal-body > table > tbody > tr:nth-child(2) > td:nth-child(3) > a') # 검색 태그 선택
    search_btn.click() # 태그 클릭
    time.sleep(4)
    '''

    # 조회날짜 선택2 - 조회날짜 선택1은 행렬로 선택을 해야 하기에 선택하기에 까다롭다
    elem = driver_chrome.find_element(By.ID, 'trdDd') # 검색 태그 선택
    # time.sleep(2)
    for _ in range(8):
        elem.send_keys(Keys.BACK_SPACE) # clear() 를 입력하면 조회일자가 이상하게 초기화되기에 backspace로 지우는 과정 추가!
    elem.send_keys(product_date)
    elem.send_keys(Keys.RETURN)
    time.sleep(4)


    # 조회 버튼 클릭
    search_btn = driver_chrome.find_element(By.ID, 'jsSearchButton') # 검색 태그 선택
    search_btn.click() # 태그 클릭
    time.sleep(4)

    # 다운로드 버튼 클릭
    search_btn = driver_chrome.find_element(By.CLASS_NAME, 'CI-MDI-UNIT-DOWNLOAD') # 검색 태그 선택
    search_btn.click() # 태그 클릭
    time.sleep(5)

    # csv 파일 다운로드 클릭
    search_btn = driver_chrome.find_elements(By.CLASS_NAME, 'ico_filedown') # 검색 태그 선택
    search_btn[1].click() # 태그 클릭
    time.sleep(4)

    filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
    shutil.move(filename,os.path.join(Initial_path,str(product_code)+"_"+str(product_date)+".csv"))


                
    # 드라이버 종료     
    driver_chrome.quit()

if __name__ == '__main__':
    crawling_selenium(20220705)

