from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# [2022.06.30] find_element_by_() 함수는 find_element(By., ) 과 같은 형태로 함수가 변경됨에 따른 추가 코드
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

Initial_path="C:\self_project\\acceleration_download_file\Download_data\pdf_files"


# 크롬 드라이버가 설치된 파일경로 설정
chromedriver = 'C:/Users/LG/dev_python/Webdriver/chromedriver.exe' # 윈도우 

# 파일 다운로드 위치 설정을 위한 코드
chromeOptions = webdriver.ChromeOptions() # 크롬 드라이버 옵션 설정
prefs = {"download.default_directory" : Initial_path} # 파일다운로드 경로 설정
chromeOptions.add_experimental_option("prefs",prefs) # 옵션 정의
driver_chrome = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions) # 설정 반영

def crawling_selenium(product_code,start_date):
    # 접속할 사이트 설정
    driver_chrome.get("https://dart.fss.or.kr/dsab007/main.do?option=corp")

    time.sleep(2)
    
    # 초기화 버튼 클릭
    reset_button = driver_chrome.find_element(By.CSS_SELECTOR,'#searchForm > div.subSearchWrap > div.btnArea > a.btnReset')
    reset_button.send_keys(Keys.ENTER)
    
    time.sleep(1)
    # 종목코드입력
    code_text = driver_chrome.find_element(By.CSS_SELECTOR,'#textCrpNm')
    code_text.clear()
    code_text.send_keys(product_code)

    time.sleep(1)
    
    # 기간 선택
    duration_button = driver_chrome.find_element(By.CSS_SELECTOR,'#date7')
    duration_button.send_keys(Keys.ENTER)
    
    time.sleep(1)
    
    # 공시유형 선택
    kind_button = driver_chrome.find_element(By.CSS_SELECTOR,'#li_01 > label:nth-child(1)> img')
    kind_button.click()
    
    time.sleep(1)
    
    # 검색버튼 선택
    search_button = driver_chrome.find_element(By.CSS_SELECTOR,'#searchForm > div.subSearchWrap > div.btnArea > a.btnSearch')
    search_button.send_keys(Keys.ENTER)
    
    time.sleep(1)
    
    
    # 모든 보고서들을 for문으로 돌려야 할듯?
    stock_report_list = driver_chrome.find_elements(By.CSS_SELECTOR,'#tbody > tr')
    for stock_report in stock_report_list[:1]:
        financial_report_link = stock_report.find_element(By.CSS_SELECTOR,'td:nth-child(3)>a')
        print(financial_report_link.get_attribute('href')) # financial_report_link.get_attribute('href') 는 'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20220816001711' 등의 사이트가 나옴!
        
        # 새로운 사이트에서의 드라이버 생성
        driver_financial = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions)
        driver_financial.get(financial_report_link.get_attribute('href')) # 사이트를 연다
        time.sleep(2)
        
        financial_report_info = driver_financial.find_element(By.ID,'19_anchor')
        financial_report_info.click()
        time.sleep(2)
        
        print('-----------------') # 이부분에서 오류가 뜸...ㄴ
        financial_report_info2 = financial_report_info.find_element(By.CLASS_NAME,'section-2')
        print(financial_report_info2)
        print('-----------------')
        time.sleep(2)
        driver_financial.quit()
    
    # 드라이버 종료     
    driver_chrome.quit()
    

if __name__ == '__main__':
    crawling_selenium('005930',20220705) # 종목코드 조회날짜