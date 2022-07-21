# 1. 라이브러리 가져오기
import pymysql


# 2. 접속하기 - 해당 데이터 베이스에 접속
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='yoy0317689*', db='snowball_database', charset='utf8') 

 

# 3. 커서 가져오기 - #cursor 는 control structure of database로, ecommerce 대신 어떤 변수명으로 하든 상관없음 
snowball=db.cursor() 


# 4. SQL 구문 만들기 (CRUD SQL 구문 등) - 따옴표를 이용해서 긴 한줄을 여러줄로 표현 
sql = '''
        INSERT INTO product_evaluate (product_ticker,product_date,per,pbr,roe, operating_to_revenue_ratio, liabilities_to_assets_ratio) VALUES(
        'test','2022-01-01',10,1,20,3,4);
    
'''

# 5. SQL 구문 실행하기 - sql 변수에 sql 명령어를 넣고 .execute()를 통해 실행
snowball.execute(sql) 

 

# 5-2. fetch__ 이용해서 데이터를 튜플 형태로 가져오기, sql 구문이 select 일 경우!
# result=snowball.fetchall()
#select *from product로 실행한 결과 중 하나만 가져올 때는 fetchone, 
 

# 6. DB에 Complete 하기

# 잘못됬을 경우 복원등 용이하게 하기 위해서삽입, 갱신, 삭제 등이 모두 끝났으면 Connection 객체의 commit() 메서드를 사용하여 데이타를 Commit함. commit을 안하면 이전까지 작업한 것이 저장이 안될 수도 있음

db.commit()


# 7. DB 연결 닫기 - 사용한 후 연결끊기
db.close() 