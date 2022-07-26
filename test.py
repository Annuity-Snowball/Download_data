product_value = [{'PER 저': {'2021-05-01': [['kospi', 57687.0], ['bank', 57489.0], ['euro', 64644.0]], '2021-06-01': [['kospi', 58671.0], ['bank', 50874.0], ['euro', 51138.0]]}}, {'PER 고': {'2021-05-01': [['energy', 145138.0], ['qqq', 149916.0]], '2021-06-01': [['energy', 145386.0], ['qqq', 144296.0]]}}]

# 전략별로 반복
for i in range(len(product_value)):
    price_strategy_key=list(product_value[i].keys())[0]
    price_strategy_value=product_value[i][price_strategy_key]
    strategy_value_keys=list(price_strategy_value.keys()) # strategy_value_keys 는 '2021-05-01' 등 날짜들
    
    
    for strategy_value_key in strategy_value_keys:
        sum=0
        price_lists=price_strategy_value[strategy_value_key]
        for price_list in price_lists:
            sum+=price_list[1]
        price_strategy_value[strategy_value_key] = sum
        


print(product_value)
        
    

