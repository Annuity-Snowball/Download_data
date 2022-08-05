import logging
from concurrent.futures import ThreadPoolExecutor
import time
import math

# 스레드 실행 함수
def task(number):
    logging.info("Sub-Thread %s: starting", number)
    result=0
    for i in range(1,number+1):
        result += i      
    logging.info("Sub-Thread %s: finishing result: %d", number, result)

    # 결과값 반환
    return result


# 메인 영역
def main():
    # Logging format 설정
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Main-Thread : before creating and running thread")
    

    # 실행 방법2

    # with context 구문 사용
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        tasks = executor.map(task, [100000000,200000000])
        
        # 결과 확인
        print(list(tasks))
        
    print("--- %s seconds ---" % (time.time() - start_time))
    logging.info("Main-Thread : all done")


# 실행하는 코드의 위치가 여기일 경우 실행
if __name__ == '__main__':
    main()