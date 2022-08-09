# 생산자 소비자를 활용한 쓰레드 구현 - 안됨..
import concurrent.futures
import logging
import queue
import random
import threading
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

Initial_path="C:\self_project\\acceleration_download_file\Download_data\pdf_files"


# 크롬 드라이버가 설치된 파일경로 설정
chromedriver = 'C:/Users/LG/dev_python/Webdriver/chromedriver.exe' # 윈도우 

# 파일 다운로드 위치 설정을 위한 코드
chromeOptions = webdriver.ChromeOptions() # 크롬 드라이버 옵션 설정
prefs = {"download.default_directory" : Initial_path} # 파일다운로드 경로 설정
chromeOptions.add_experimental_option("prefs",prefs) # 옵션 정의

# 생산자
def producer(product_code,product_date):
    """네트워크 대기 상태라 가정(서버) , 크롤링, 파일 읽어오기 등의 역할"""
    while not event.is_set() and pipeline.not_full:
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
        
        print()
        print("-----------------------------------------------------------------")
        print("In Producer",product_code,product_date)
        print(stock_list)
        
        # 큐에 값을(크롤링한 리스트) 넣음
        pipeline.put(stock_list)
        print('count 전 :',count)
        count+=1
        print('count 후 :',count)
    logging.info("Producer received event. Exiting")

# 소비자
def consumer():
    """응답 받고 소비하는 것으로 가정 or DB 저장"""
    while not event.is_set() or not pipeline.empty(): # while((false)or(false)) 여야지 무한반복이 멈춤으로, 큐에 있는 값들을                                                                                    다 내보낸다! 
        stock_list = pipeline.get()
        print()
        print("-----------------------------------------------------------------")
        print("In Consumer")
        print(stock_list)

    logging.info("Consumer received event. Exiting")


def main():

   

    # With Context 시작
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        
        executor.map(producer, product_code_list, product_date_list)
        executor.submit(consumer)

        # 실행 시간 조정
        time.sleep(0.1)

        print("count in with:",count)
        # 프로그램 종료 - set을 하면 flag 값이 1이 됨으로, producer랑 comsumer가 1을 받으면 종료하게 코드를 짤 예정
        if count == len(product_code_list):
            event.set()
        
# 실행하는 코드의 위치가 여기일 경우 실행
if __name__ == '__main__':
     # 사이즈 중요, queue를 지정
    pipeline = queue.Queue(maxsize=10) # maxsize가 핵심, 메모리 상태에 따라서 size를 조절해줘야 한다

    # 이벤트 플래그 초기 값 0
    event = threading.Event() # threading 패키지에서 Event 객체를 가져옴
    
    count = 0
    
    product_code_list = [395750,269530,295820,429740,433850,161510] # [395750,269530,295820,429740,433850,161510,189400,429760,287180,280920,227830]
    product_date_list = [20220705,20220607,20220613,20220705,20220805,20220613] # [20220705,20220607,20220613,20220705,20220805,20220613,20220705,20220606,20220613,20220705,20220606]
    
    # 시간 측정
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))