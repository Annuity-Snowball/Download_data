# 멀티프로세스로 구현

from concurrent.futures import ProcessPoolExecutor
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# [2022.06.30] find_element_by_() 함수는 find_element(By., ) 과 같은 형태로 함수가 변경됨에 따른 추가 코드
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


Initial_path="C:\self_project\\acceleration_download_file\Download_data\pdf_files"


# 크롬 드라이버가 설치된 파일경로 설정
chromedriver = 'C:/Users/LG/dev_python/Webdriver/chromedriver.exe' # 윈도우 

# 파일 다운로드 위치 설정을 위한 코드
chromeOptions = webdriver.ChromeOptions() # 크롬 드라이버 옵션 설정
prefs = {"download.default_directory" : Initial_path} # 파일다운로드 경로 설정
chromeOptions.add_experimental_option("prefs",prefs) # 옵션 정의


# 스레드 실행 함수
def crawling_selenium(product_code,product_date):
    print(f"상품코드 : {product_code}, 조회날짜 : {product_date} 시작!")
    # 접속할 사이트 설정
    driver_chrome = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions) # 설정 반영
    driver_chrome.get("http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030108")



    # 처음 사이트 들어간 후 4초 대기
    time.sleep(4)


    # 금융상품명 검색 버튼 클릭
    search_btn = driver_chrome.find_element(By.ID, 'btnisuCd_finder_secuprodisu1_0') # 검색 태그 선택
    search_btn.click() # 태그 클릭
    time.sleep(4)

    # 금융상품코드를 통해서 금융상품 선택
    search_bar = driver_chrome.find_element(By.CSS_SELECTOR,'#searchText__finder_secuprodisu1_0') # 검색 창 선택
    search_bar.clear()
    search_bar.send_keys(product_code)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(4)
    

    # 조회날짜 선택 
    elem = driver_chrome.find_element(By.ID, 'trdDd') # 검색 태그 선택
    for _ in range(8):
        elem.send_keys(Keys.BACK_SPACE) # clear() 를 입력하면 조회일자가 이상하게 초기화되기에 backspace로 지우는 과정 추가!
    elem.send_keys(product_date)
    elem.send_keys(Keys.RETURN)
    time.sleep(4)


    # 조회 버튼 클릭
    search_btn = driver_chrome.find_element(By.ID, 'jsSearchButton') # 검색 태그 선택
    search_btn.click() # 태그 클릭
    time.sleep(4)
    
    
    # 금융상품의 구성 종목 조회 - 일단 10개의 종목만 받아옴
    stock_list=list()
    stock_infos = driver_chrome.find_elements(By.CSS_SELECTOR,'#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table > tbody > tr')
    for stock_info in stock_infos:
        # 종목명이 띄어쓰기로 이루어져 있는 경우도 있다
        temp_list = stock_info.text.split()
        temp_list[1]=" ".join(temp_list[1:-4])
        del temp_list[2:-4]
        stock_list.append(temp_list)
    
    # 드라이버 종료     
    driver_chrome.quit()
    print(stock_list)
    return stock_list


# 메인 영역
def main():

    product_code_list = [395750,269530,295820,429740,433850,161510,189400,429760,287180,280920,227830]
    product_date_list = [20220705,20220607,20220613,20220705,20220805,20220613,20220705,20220606,20220613,20220705,20220606]
    # with context 구문 사용
    with ProcessPoolExecutor(max_workers=5) as executor:
        tasks = executor.map(crawling_selenium, product_code_list, product_date_list)
        
        # 결과 확인
        # print(list(tasks))



# 실행하는 코드의 위치가 여기일 경우 실행
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))