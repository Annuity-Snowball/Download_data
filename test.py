product_count=[{'PER 저': {'2021-01-01': [['euro', 11], ['china', 7], ['energy', 7]]}}, {'PER 고': {'2021-01-01': [['qqq', 25], ['spy', 25]]}}]
new_date='2021-01-15'

for i in range(len(product_count)):
    price_strategy_key=list(product_count[i].keys())[0]
    price_strategy_value=product_count[i][price_strategy_key]
    price_strategy_value[new_date]=price_strategy_value.pop(list(price_strategy_value.keys())[0])
print(product_count)