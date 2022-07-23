input_money = 300000
stratgy_ratio=[40,60]
portfolio_product_count=[{'PER 저': {'2021-01-01': [['bank', 1269.0], ['energy', 4456.0], ['kospi', 22654.0]], '2021-02-01': [['bank', 1853.0], ['kospi', 26166.0], ['energy', 4145.0]], '2021-03-01': [['bank', 2048.0], ['kospi', 14086.0], ['energy', 3491.0]]}}, {'PER 고': {'2021-01-01': [['china', 5248.0], ['spy', 26202.0]], '2021-02-01': [['china', 7087.0], ['bio', 24193.0]], '2021-03-01': [['china', 5952.0], ['bio', 12482.0]]}}]

input_money_ratio=list()
for i in stratgy_ratio:
    input_money_ratio.append(i*input_money//100)

print('input_money_ratio :',input_money_ratio)

'''
# stratgy_keys = list(portfolio_product_price[i].keys())[0] -> i를 변경시키면서 '현금', 'PER 저' 등 가져올수 있음!
# product_price_dict = list(portfolio_product_price[i].values())[0] -> i를 변경시기면서 {'2021-01-01': [['bank', 1269.0], ['energy', 4456.0], ['kospi', 22654.0]], '2021-02-01': [['bank', 1853.0], ['kospi', 26166.0], ['energy', 4145.0]], '2021-03-01': [['bank', 2048.0], ['kospi', 14086.0], ['energy', 3491.0]]}
# product_price_dict_keys = list(product_price_dict.keys()) -> ['2021-01-01', '2021-02-01', '2021-03-01']
product_price_dict=list(portfolio_product_count[0].values())[0] # {'2021-01-01': [['bank', 1269.0], ['energy', 4456.0], ['kospi', 22654.0]], '2021-02-01': [['bank', 1853.0], ['kospi', 26166.0], ['energy', 4145.0]], '2021-03-01': [['bank', 2048.0], ['kospi', 14086.0], ['energy', 3491.0]]}
product_price_dict_keys = list(product_price_dict.keys()) # ['2021-01-01', '2021-02-01', '2021-03-01']
print(product_price_dict[product_price_dict_keys[0]]) # [['bank', 1269.0], ['energy', 4456.0], ['kospi', 22654.0]]
for price_list in product_price_dict[product_price_dict_keys[0]]:
    print(price_list[0]) # bank
    print(price_list[1]) # 1269.0
'''


print('before portfolio_product_count', portfolio_product_count)
# 전략별로 돌면서 실행
for i,money in enumerate(input_money_ratio):
    stratgy_key = list(portfolio_product_count[i].keys())[0]
    product_price_dict = list(portfolio_product_count[i].values())[0]
    product_price_dict_keys = list(product_price_dict.keys())
    print('stratgy_key :', stratgy_key)
    print('product_price_dict :', product_price_dict)
    print('product_price_dict_keys :', product_price_dict_keys)
    print('money :', money)
    print()
    for product_price_dict_key in product_price_dict_keys:
        print('money2 :',money)
        price_lists=product_price_dict[product_price_dict_key] # [['bank', 2048.0], ['kospi', 14086.0], ['energy', 3491.0]] 
        print('price_lists :', price_lists)
        money_to_price_list = money//len(price_lists)
        print('money_to_price_list :',money_to_price_list)
        for price_list in price_lists:
            price_list[1] = int(money_to_price_list // price_list[1])
            print('price_list', price_list)
    print('after product_price_dict :', product_price_dict)
    
    
    print()

print('after portfolio_product_count', portfolio_product_count)