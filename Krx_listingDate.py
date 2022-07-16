from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import shutil

Initial_path = "C:\\Users\pth99\OneDrive\Desktop\\annuity_snowball"

# 크롬 드라이버가 설치된 파일경로 설정
chromedriver = 'C:\\Users\pth99\OneDrive\Desktop/chromedriver.exe'  # 윈도우

# 파일 다운로드 위치 설정을 위한 코드
chromeOptions = webdriver.ChromeOptions()  # 크롬 드라이버 옵션 설정
prefs = {"download.default_directory": Initial_path}  # 파일다운로드 경로 설정
chromeOptions.add_experimental_option("prefs", prefs)  # 옵션 정의
driver_chrome = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions)  # 설정 반영

# 접속할 사이트 설정
driver_chrome.get("http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030204")

# 처음 사이트 들어간 후 4초 대기
time.sleep(4)


# 다운로드 버튼 클릭
search_btn = driver_chrome.find_element(By.CLASS_NAME, 'CI-MDI-UNIT-DOWNLOAD')  # 검색 태그 선택
search_btn.click()  # 태그 클릭
time.sleep(5)

# csv 파일 다운로드 클릭
search_btn = driver_chrome.find_elements(By.CLASS_NAME, 'ico_filedown')  # 검색 태그 선택
search_btn[1].click()  # 태그 클릭
time.sleep(4)

filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)], key=os.path.getctime)
shutil.move(filename, os.path.join(Initial_path, "date" + ".csv"))

# 드라이버 종료
driver_chrome.quit()