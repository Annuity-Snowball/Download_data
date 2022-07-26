portfolio_strategy_value = [{'PER 저': {'2021-05-01': 179820.0, '2021-06-01': 160683.0}}, {'PER 고': {'2021-05-01': 295054.0, '2021-06-01': 289682.0}}]

portfolio_value=dict()

# 전략별로 반복
for i in range(len(portfolio_strategy_value)):
    price_strategy_key=list(portfolio_strategy_value[i].keys())[0]
    price_strategy_value=portfolio_strategy_value[i][price_strategy_key]
    strategy_value_keys=list(price_strategy_value.keys()) # strategy_value_keys 는 '2021-05-01' 등 날짜들
    
    
    for strategy_value_key in strategy_value_keys:
        if strategy_value_key in portfolio_value:
            portfolio_value[strategy_value_key]+=price_strategy_value[strategy_value_key]
        else:
            portfolio_value[strategy_value_key]=price_strategy_value[strategy_value_key]
print(portfolio_value)