result=list()
for interval_date in range(2000,2100):

    # get_stratgy_price_query 는 전략종류에 따라서 가져온 금융상품의 정보(금융상품티커) 을 가져오는 쿼리
    get_product_ticker_query='select product_date,product_ticker from product_evaluate order by per asc limit 3'.split(' ')
    get_product_ticker_query.insert(4,"where product_date = '"+str(interval_date)+"'") # str(20200101) 은 interval_dates들을 반복문으로 대입
    get_product_ticker_query=" ".join(get_product_ticker_query)

    print('get_product_ticker_query :',get_product_ticker_query)
    
    # SQL 구문 실행하기 - sql 변수에 sql 명령어를 넣고 .execute()를 통해 실행
    snowball.execute(get_product_ticker_query) 
    
    # sql 결과값들로 조회한 값들을 anwers에 담음
    answers=list(snowball.fetchall())
    for i in range(len(answers)):
        answers[i] = list(answers[i])
        answers[i][0] = str(answers[i][0])
    result.append(answers)