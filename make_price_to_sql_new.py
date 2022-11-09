# 1. 라이브러리 가져오기
import pymysql
import os
# 2. 접속하기 - 해당 데이터 베이스에 접속
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='yoy0317689*', db='snowball_database', charset='utf8') 

snowball=db.cursor() 

# 4. SQL 구문 만들기 (CRUD SQL 구문 등) - 따옴표를 이용해서 긴 한줄을 여러줄로 표현 
sql_list=list()
product_lists = list()
file_lists = os.listdir('C:\\self_project\\snowball\\Download_data\\product_price')

for filename in file_lists:
    product_lists.append(filename.split('_')[0])


# product_lists = ['bank','bio','china','energy','euro','kospi','qqq','spy']

# personal_info 테이블 생성
sql_list.append("""
        CREATE TABLE peronal_info(
        user_id varchar(20),
        user_name varchar(20),
        user_nickname varchar(20),
        user_password varchar(20), 
        PRIMARY KEY(user_id)
        );
""")

# portfolio_info 테이블 생성
sql_list.append("""
        CREATE TABLE portfolio_info(
        portfolio_id varchar(20),
        user_id varchar(20),
        portfolio_name varchar(20),
        strategy_count int,
        start_date date,
        end_date date, 
        rebalance_cycle int, 
        input_type varchar(5), 
        input_money int,
        PRIMARY KEY(portfolio_id)
        );
""")

# portfolio_product_1 테이블 생성
sql_list.append("""
        CREATE TABLE portfolio_product_1(
        id int Auto_Increment Primary Key,
        portfolio_id varchar(20),
        portfolio_date date,
        product_ticker_1 varchar(20)
        );
""")

# portfolio_product_2 테이블 생성
sql_list.append("""
        CREATE TABLE portfolio_product_2(
        id int Auto_Increment Primary Key,
        portfolio_id varchar(20), 
        portfolio_date date, 
        product_ticker_1 varchar(20), 
        product_ticker_2 varchar(20)
        );
""")

# portfolio_product_3 테이블 생성
sql_list.append("""
        CREATE TABLE portfolio_product_3(
        id int Auto_Increment Primary Key, 
        portfolio_id varchar(20), 
        portfolio_date date, 
        product_ticker_1 varchar(20), 
        product_ticker_2 varchar(20), 
        product_ticker_3 varchar(20)
        );
""")

# portfolio_product_4 테이블 생성
sql_list.append("""
        CREATE TABLE portfolio_product_4(
        id int Auto_Increment Primary Key, 
        portfolio_id varchar(20), 
        portfolio_date date, 
        product_ticker_1 varchar(20), 
        product_ticker_2 varchar(20), 
        product_ticker_3 varchar(20), 
        product_ticker_4 varchar(20)
        );
""")

# portfolio_product_5 테이블 생성
sql_list.append("""
        CREATE TABLE portfolio_product_5(
        id int Auto_Increment Primary Key, 
        portfolio_id varchar(20), 
        portfolio_date date, 
        product_ticker_1 varchar(20), 
        product_ticker_2 varchar(20), 
        product_ticker_3 varchar(20), 
        product_ticker_4 varchar(20), 
        product_ticker_5 varchar(20)
        );
""")

# portfolio_result 테이블 생성
sql_list.append("""
        CREATE TABLE portfolio_result(
        portfolio_id varchar(20) Primary Key, 
        result_money int, 
        accumulated_earning_rate float, 
        year_average_earning_rate float, 
        mdd float, 
        victory_rate float, 
        year_high_earning_rate float, 
        year_low_earning_rate float, 
        year_by_year_earning_rate varchar(50), 
        receive_duration int, 
        receive_money int, 
        tax_credit varchar(3)
        );
""")

# portfolio_stratgy_1 테이블 생성
sql_list.append("""
        CREATE TABLE portfolio_stratgy_1(
        portfolio_id varchar(20) Primary Key,
        stratgy_kind_1 varchar(20)
        );
""")

# portfolio_stratgy_2 테이블 생성
sql_list.append("""
        CREATE TABLE portfolio_stratgy_2(
        portfolio_id varchar(20) Primary Key, 
        stratgy_kind_1 varchar(20), 
        stratgy_kind_2 varchar(20), 
        stratgy_kind_ratio_1 float, 
        stratgy_kind_ratio_2 float
        );
""")

# portfolio_stratgy_3 테이블 생성
sql_list.append("""
        CREATE TABLE portfolio_stratgy_3(
        portfolio_id varchar(20) Primary Key, 
        stratgy_kind_1 varchar(20), 
        stratgy_kind_2 varchar(20), 
        stratgy_kind_3 varchar(20), 
        stratgy_kind_ratio_1 float, 
        stratgy_kind_ratio_2 float, 
        stratgy_kind_ratio_3 float
        );
""")

# portfolio_stratgy_4 테이블 생성
sql_list.append("""
        CREATE TABLE portfolio_stratgy_4(
        portfolio_id varchar(20) Primary Key, 
        stratgy_kind_1 varchar(20), 
        stratgy_kind_2 varchar(20), 
        stratgy_kind_3 varchar(20), 
        stratgy_kind_4 varchar(20), 
        stratgy_kind_ratio_1 float, 
        stratgy_kind_ratio_2 float, 
        stratgy_kind_ratio_3 float, 
        stratgy_kind_ratio_4 float
        );
""")

# portfolio_stratgy_5 테이블 생성
sql_list.append("""
        CREATE TABLE portfolio_stratgy_5(
        portfolio_id varchar(20) Primary Key,  
        stratgy_kind_1 varchar(20), 
        stratgy_kind_2 varchar(20), 
        stratgy_kind_3 varchar(20), 
        stratgy_kind_4 varchar(20), 
        stratgy_kind_5 varchar(20), 
        stratgy_kind_ratio_1 float, 
        stratgy_kind_ratio_2 float, 
        stratgy_kind_ratio_3 float, 
        stratgy_kind_ratio_4 float, 
        stratgy_kind_ratio_5 float
        );
""")

# price_ 테이블들 추가
for product in product_lists:
    sql_list.append("""
        CREATE TABLE price_"""+product+"""(
        product_date date Primary Key, 
        high_price float, 
        low_price float, 
        start_price float, 
        end_price float
        );
""")

# product_evaluate 테이블 생성
sql_list.append("""
        CREATE TABLE product_evaluate(
        id int Auto_Increment Primary Key, 
        product_ticker varchar(20), 
        product_date date, 
        per float, 
        pbr float, 
        roe float, 
        operating_to_revenue_ratio float, 
        liabilities_to_assets_ratio float
        );
""")

# product_finance 테이블 생성
sql_list.append("""
        CREATE TABLE product_finance(
        id int Auto_Increment Primary Key, 
        product_ticker varchar(20), 
        stock_date date, 
        revenue float, 
        gross_profit float, 
        operation_income float, 
        net_income float, 
        total_assets float, 
        total_liabilities float, 
        total_equity float, 
        current_assets float, 
        current_liabilities float, 
        operating_cashflow float, 
        free_cashflow float, 
        dividends float
        );
""")


# product_info 테이블 생성
sql_list.append("""
        CREATE TABLE product_info(
        product_ticker varchar(10) Primary Key, 
        product_date date, 
        top1_stock_ticker varchar(10), 
        top2_stock_ticker varchar(10), 
        top3_stock_ticker varchar(10),
        top4_stock_ticker varchar(10), 
        top5_stock_ticker varchar(10), 
        top6_stock_ticker varchar(10), 
        top7_stock_ticker varchar(10), 
        top8_stock_ticker varchar(10), 
        top9_stock_ticker varchar(10), 
        top10_stock_ticker varchar(10), 
        top1_stock_ratio float, 
        top2_stock_ratio float, 
        top3_stock_ratio float, 
        top4_stock_ratio float, 
        top5_stock_ratio float, 
        top6_stock_ratio float, 
        top7_stock_ratio float, 
        top8_stock_ratio float, 
        top9_stock_ratio float, 
        top10_stock_ratio float
        );
""")

# product_kind 테이블 생성
sql_list.append("""
        CREATE TABLE product_kind(
        product_ticker varchar(10) Primary Key, 
        product_name varchar(10), 
        product_category varchar(15), 
        product_base_ticker varchar(10)
        );
""")

# stock_finance 테이블 생성
sql_list.append("""
        CREATE TABLE stock_finance(
        id int Auto_Increment Primary Key, 
        stock_ticker varchar(20), 
        stock_date date, 
        revenue float, 
        gross_profit float, 
        operation_income float, 
        net_income float, 
        total_assets float, 
        total_liabilities float, 
        total_equity float, 
        current_assets float, 
        current_liabilities float, 
        operating_cashflow float, 
        free_cashflow float, 
        dividends float
        );
""")


for sql in sql_list:
    print(sql)
    # 5. SQL 구문 실행하기 - sql 변수에 sql 명령어를 넣고 .execute()를 통해 실행
    snowball.execute(sql) 


    # 6. DB에 Complete 하기

    # 잘못됬을 경우 복원등 용이하게 하기 위해서삽입, 갱신, 삭제 등이 모두 끝났으면 Connection 객체의 commit() 메서드를 사용하여 데이타를 Commit함. commit을 안하면 이전까지 작업한 것이 저장이 안될 수도 있음

    db.commit()


# 7. DB 연결 닫기 - 사용한 후 연결끊기
db.close() 
