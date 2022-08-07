from concurrent.futures import ProcessPoolExecutor, as_completed
import urllib.request

# 조회 URLS
URLS = ['http://www.daum.net/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']

# 실행 함수
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn: # timeout 시간 내에 url 사이트를 방문해서
        return conn.read() # 방문한 페이지 소스를 읽어옴

def main():
    # 프로세스풀 Context 영역
    with ProcessPoolExecutor(max_workers=5) as executor:
        

        # Future 로드(실행X, 예약만 함)
        future_to_url = {executor.submit(load_url, url, 60): url for url in URLS} # dict 형태, {key : value}
        
        # 중간 확인(Dict)
        # print(future_to_url)
        
        # 실행
        for future in as_completed(future_to_url): # timeout=1(테스트 추천), dict는 반복문에서 key값들을 반환
            # Key값이 Future 객체
            url = future_to_url[future] # future_to_url.get()으로 겨와도 됨
            try:
                # 결과
                data = future.result()
            except Exception as exc:
                # 예외 처리
                print('%r generated an exception: %s' % (url, exc))
            else: # try에서 에러 없으면 else 문 실행
                # 결과 확인
                print('%r page is %d bytes' % (url, len(data)))

# 메인 시작
if __name__ == '__main__':
    main()