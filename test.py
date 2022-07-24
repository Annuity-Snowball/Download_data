rebalance_balance_account=dict()
input_money=1000000
# input_money_ratio_list=[[] for _ in range(len(input_money_list))]
strategy_ratio=[40,60]
input_money_ratio=list()
portfolio_rebalance_product_count=[{'PER 저': {'2021-01-01': [['bank', 1269.0], ['energy', 4456.0], ['kospi', 22654.0]], '2021-07-01': [['bank', 2254.0], ['kospi', 11893.0], ['euro', 28164.0]], '2022-01-01': [['bank', 2518.0], ['energy', 3720.0], ['kospi', 28933.0]]}}, {'PER 고': {'2021-01-01': [['china', 5248.0], ['spy', 26202.0]], '2021-07-01': [['china', 6837.0], ['bio', 26904.0]], '2022-01-01': [['china', 6562.0], ['bio', 22386.0]]}}]

# for i,input_money in enumerate(input_money_list):
for i,amount in enumerate(strategy_ratio):
    input_money_ratio.append(amount*input_money//100)

print(input_money_ratio)

print('before portfolio_rebalance_product_count',portfolio_rebalance_product_count)

# for i,input_money_ratio in enumerate(input_money_ratio_list): # input_money_ratio_list 는 [[400000, 600000], [800000, 1200000], [1200000, 1800000]] 
#전략별로 반복
for i,strategy_kind_money in enumerate(input_money_ratio): # input_money_ratio 는 ex) [400000, 600000], strategy_kind_money는 한 전략을 구입할 금액
    product_price_dict = list(portfolio_rebalance_product_count[0].values())[0]
    product_price_dict_keys = list(product_price_dict.keys()) # ['2021-01-01', '2021-07-01', '2022-01-01']
    price_lists=product_price_dict[product_price_dict_keys[0]]
    
    if i ==0:
        rebalance_balance_account[product_price_dict_keys[0]]=0
        
    # print('strategy_kind_money :', strategy_kind_money)
    # print('price_lists :', price_lists)
    strategy_product_money = int(strategy_kind_money // len(price_lists)) # strategy_product_money 는 전략에 해당하는 금융상품들중 한 금융상품을 구입할 금액
    # print('strategy_product_money :', strategy_product_money)
    # print('before balance_account : ',balance_account)
    for price_list in price_lists:
        # print('price_list[1] :',price_list[1])
        rebalance_balance_account[product_price_dict_keys[0]] += strategy_product_money%price_list[1]
        # print('after balance_account : ',balance_account)
        price_list[1] = int(strategy_product_money//price_list[1])
        
    # print('after price_lists :', price_lists)
    # print()
print(rebalance_balance_account)
print('after portfolio_rebalance_product_count',portfolio_rebalance_product_count)