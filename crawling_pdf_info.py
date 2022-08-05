import logging
from concurrent.futures import ThreadPoolExecutor
import time

# 스레드 실행 함수
def task(name):
    logging.info("Sub-Thread %s: starting", name)
    result = 0

    # 스레드에서 구현할 함수?
    for i in range(10001):
        result = result + i
    logging.info("Sub-Thread %s: finishing result: %d", name, result)

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

    with ThreadPoolExecutor(max_workers=3) as executor:
        tasks = executor.map(task, ['First', 'Second'])
        
        # 결과 확인
        print(list(tasks))

    logging.info("Main-Thread : all done")


# 실행하는 코드의 위치가 여기일 경우 실행
if __name__ == '__main__':
    main()