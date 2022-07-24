portfolio_product_count=[{'PER 저': {'2021-01-01': [['bank', 1269.0], ['energy', 4456.0], ['kospi', 22654.0]], '2021-02-01': [['bank', 1853.0], ['energy', 4145.0], ['kospi', 26166.0]], '2021-03-01': [['bank', 2048.0], ['energy', 3491.0], ['kospi', 14086.0]], '2021-04-01': [['bank', 2287.0], ['energy', 4060.0], ['kospi', 13185.0]]}}, {'PER 고': {'2021-01-01': [['china', 5248.0], ['spy', 26202.0]], '2021-02-01': [['china', 7087.0], ['spy', 25745.0]], '2021-03-01': [['china', 5952.0], ['spy', 29603.0]], '2021-04-01': [['china', 7963.0], ['spy', 20850.0]]}}]
    
input_balance_account=dict()

input_money_ratio=list()
input_money = 200000
for i in [40,60]:
    input_money_ratio.append(i*input_money//100)

print('input_money_ratio :',input_money_ratio)
print('before portfolio_product_count :', portfolio_product_count)
# 전략별로 돌면서 실행
for i,money in enumerate(input_money_ratio):
    product_price_dict = list(portfolio_product_count[i].values())[0]
    # print('product_price_dict :', product_price_dict) # {'2021-01-01': [['bank', 1269.0], ['energy', 4456.0], ['kospi', 22654.0]], '2021-02-01': [['bank', 1853.0], ['energy', 4145.0], ['kospi', 26166.0]], '2021-03-01': [['bank', 2048.0], ['energy', 3491.0], ['kospi', 14086.0]], '2021-04-01': [['bank', 2287.0], ['energy', 4060.0], ['kospi', 13185.0]]}
    product_price_dict_keys = list(product_price_dict.keys())
    # print('product_price_dict_keys :', product_price_dict_keys) #  ['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01']
    
        
    for product_price_dict_key in product_price_dict_keys:
        if i ==0:
            input_balance_account[product_price_dict_key]=0
        price_lists=product_price_dict[product_price_dict_key] # [['bank', 2048.0], ['kospi', 14086.0], ['energy', 3491.0]] 
        # print('price_lists :',price_lists)
        money_to_price_list = money//len(price_lists)
        # print('money_to_price_list :',money_to_price_list)
        for price_list in price_lists:
            input_balance_account[product_price_dict_key] += money_to_price_list % price_list[1]
            price_list[1] = int(money_to_price_list // price_list[1])
    # print()
print()
print('after portfolio_product_count :', portfolio_product_count)
print()
print('input_balance_account :', input_balance_account)
