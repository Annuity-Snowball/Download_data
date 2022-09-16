# 1. 라이브러리 가져오기
import pymysql
import datetime
import random

# 2. 접속하기 - 해당 데이터 베이스에 접속
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='yoy0317689*', db='snowball_database', charset='utf8') 


# 기간동안의 모든 날짜들을 구하기 위한 함수
date_lists=list()
# per_list = list()
# pbr_list = list()
# roe_list = list()
# operating_to_revenue_ratio_list = list()
# liabilities_to_assets_ratio_list = list()

date = datetime.datetime(2016,12,31,12,4,5)
for i in range(1826): 
    date += datetime.timedelta(days=1)
    date_lists.append(str(date).split()[0])
 
    
        
product_lists = ['bank','bio','china','energy','euro','kospi','qqq','spy']

# 3. 커서 가져오기 - #cursor 는 control structure of database로, ecommerce 대신 어떤 변수명으로 하든 상관없음 
snowball=db.cursor() 

for date_list in date_lists:
        for product_list in product_lists:
                # 4. SQL 구문 만들기 (CRUD SQL 구문 등) - 따옴표를 이용해서 긴 한줄을 여러줄로 표현
                per_num = random.uniform(8, 20)
                per_num = round(per_num,2) 
                
                pbr_num = random.uniform(0.8, 3)
                pbr_num = round(pbr_num,2) 
                
                roe_num = random.uniform(10, 25)
                roe_num = round(roe_num,2)
                
                operating_to_revenue_ratio = random.uniform(0.05, 0.3)
                operating_to_revenue_ratio = round(operating_to_revenue_ratio,2)
                
                liabilities_to_assets_ratio = random.uniform(30, 80)
                liabilities_to_assets_ratio = round(liabilities_to_assets_ratio,2)
                
                sql = """
                        INSERT INTO product_evaluate (product_ticker, product_date, per, pbr, roe, operating_to_revenue_ratio, liabilities_to_assets_ratio) VALUES
                        ('"""+product_list+"""','"""+date_list+"""', """+str(per_num)+""", """+str(pbr_num)+""", """+str(roe_num)+""", 
                        """+str(operating_to_revenue_ratio)+""", """+str(liabilities_to_assets_ratio)+"""); 
                """
                
                print(sql)
                # 5. SQL 구문 실행하기 - sql 변수에 sql 명령어를 넣고 .execute()를 통해 실행
                snowball.execute(sql) 

                

                # 6. DB에 Complete 하기

                # 잘못됬을 경우 복원등 용이하게 하기 위해서삽입, 갱신, 삭제 등이 모두 끝났으면 Connection 객체의 commit() 메서드를 사용하여 데이타를 Commit함. commit을 안하면 이전까지 작업한 것이 저장이 안될 수도 있음

                db.commit()


# 7. DB 연결 닫기 - 사용한 후 연결끊기
db.close() 