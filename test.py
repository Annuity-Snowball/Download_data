# 복사를 통해서 portfolio_history 생성
portfolio_product_count=[{'PER 저': {'2021-01-01': [['bank', 1269.0], ['energy', 4456.0], ['kospi', 22654.0]], '2021-07-01': [['bank', 2254.0], ['kospi', 11893.0], ['euro', 28164.0]], '2022-01-01': [['bank', 2518.0], ['energy', 3720.0], ['kospi', 28933.0]]}}, 
                         {'PER 고': {'2021-01-01': [['china', 5248.0], ['spy', 26202.0]], '2021-07-01': [['china', 6837.0], ['bio', 26904.0]], '2022-01-01': [['china', 6562.0], ['bio', 22386.0]]}}]

input_money_list=[1000000,2000000,3000000]
strategy_ratio = [40,60]

balance_account=dict()

input_money_ratio_list=[[] for _ in range(len(input_money_list))]

for i,input_money in enumerate(input_money_list):
    for amount in strategy_ratio:
        input_money_ratio_list[i].append(amount*input_money//100)

print(input_money_ratio_list) # [[400000, 600000], [800000, 1200000], [1200000, 1800000]]


'''
product_price_dict = list(portfolio_product_count[0].values())[0]
print('product_price_dict :',product_price_dict) #  {'2021-01-01': [['bank', 1269.0], ['energy', 4456.0], ['kospi', 22654.0]], '2021-07-01': [['bank', 2254.0], ['kospi', 11893.0], ['euro', 28164.0]], '2022-01-01': [['bank', 2518.0], ['energy', 3720.0], ['kospi', 28933.0]]}
product_price_dict_keys = list(product_price_dict.keys())
print('product_price_dict_keys :',product_price_dict_keys) #  ['2021-01-01', '2021-07-01', '2022-01-01']
price_lists=product_price_dict[product_price_dict_keys[0]] 
print('price_lists :',price_lists) # [['bank', 1269.0], ['energy', 4456.0], ['kospi', 22654.0]]
'''
# 리밸런싱 날짜별로 반복
for i,input_money_ratio in enumerate(input_money_ratio_list): # input_money_ratio_list 는 [[400000, 600000], [800000, 1200000], [1200000, 1800000]] 
    #전략별로 반복
    for j,strategy_kind_money in enumerate(input_money_ratio): # input_money_ratio 는 ex) [400000, 600000], strategy_kind_money는 한 전략을 구입할 금액
        product_price_dict = list(portfolio_product_count[j].values())[0]
        product_price_dict_keys = list(product_price_dict.keys()) # ['2021-01-01', '2021-07-01', '2022-01-01']
        price_lists=product_price_dict[product_price_dict_keys[i]]
        
        if j ==0:
            balance_account[product_price_dict_keys[i]]=0
            
        print('strategy_kind_money :', strategy_kind_money)
        print('price_lists :', price_lists)
        strategy_product_money = int(strategy_kind_money // len(price_lists)) # strategy_product_money 는 전략에 해당하는 금융상품들중 한 금융상품을 구입할 금액
        print('strategy_product_money :', strategy_product_money)
        print('before balance_account : ',balance_account)
        for price_list in price_lists:
            print('price_list[1] :',price_list[1])
            balance_account[product_price_dict_keys[i]] += strategy_product_money%price_list[1]
            print('after balance_account : ',balance_account)
            price_list[1] = int(strategy_product_money//price_list[1])
            
        print('after price_lists :', price_lists)
        print()
print(balance_account)
print(portfolio_product_count)