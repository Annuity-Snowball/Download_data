portfolio_rebalance_product_count=[{'PER 저': {'2021-04-01': [['kospi', 11], ['bank', 11], ['euro', 12]]}}, {'PER 고': {'2021-04-01': [['energy', 18], ['qqq', 23]]}}]
portfolio_product_count=[{'PER 저': {'2021-05-01': [['kospi', 3], ['bank', 3], ['euro', 6]]}}, {'PER 고': {'2021-05-01': [['energy', 14], ['qqq', 12]]}}]

 # 전략별로 반복
for i in range(len(portfolio_product_count)):
    product_strategy_key=list(portfolio_product_count[i].keys())[0]
    product_strategy_value=portfolio_product_count[i][product_strategy_key]
    product_strategy_value_key=list(product_strategy_value.keys())[0] # strategy_value_keys 는 '2021-05-01' 등 날짜들
    
    rebalance_product_strategy_key=list(portfolio_rebalance_product_count[i].keys())[0]
    rebalance_product_strategy_value=portfolio_rebalance_product_count[i][rebalance_product_strategy_key]
    rebalance_product_strategy_value_key=list(rebalance_product_strategy_value.keys())[0]
    
    for i,product_list in enumerate(product_strategy_value[product_strategy_value_key]):
        product_list[1]+=rebalance_product_strategy_value[rebalance_product_strategy_value_key][i][1]
    
    
print(portfolio_product_count)