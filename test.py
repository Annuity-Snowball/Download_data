product_price = [{'PER 저': {'2021-05-01': [['kospi', 19229.0], ['bank', 19163.0], ['euro', 10774.0]], '2021-06-01': [['kospi', 19557.0], ['bank', 16958.0], ['euro', 17046.0]]}}, {'PER 고': {'2021-05-01': [['energy', 10367.0], ['qqq', 12493.0]], '2021-06-01': [['energy', 16154.0], ['qqq', 18037.0]]}}]
product_count = [{'PER 저': {'2021-05-01': [['kospi', 3], ['bank', 3], ['euro', 6]], '2021-06-01': [['kospi', 3], ['bank', 3], ['euro', 3]]}}, {'PER 고': {'2021-05-01': [['energy', 14], ['qqq', 12]], '2021-06-01': [['energy', 9], ['qqq', 8]]}}]

# product_price, product_count와 비슷한 구조
product_value = list()

for i in range(len(product_price)):
    price_strategy_key=list(product_price[i].keys())[0]
    price_strategy_value=product_price[i][price_strategy_key]
    strategy_value_keys=list(price_strategy_value.keys())
    
    count_strategy_value=product_count[i][price_strategy_key]
    
    for strategy_value_key in strategy_value_keys:
        price_lists=price_strategy_value[strategy_value_key]
        count_lists=count_strategy_value[strategy_value_key]
        
        for i in range(len(price_lists)):
            price_lists[i][1] = price_lists[i][1] * count_lists[i][1]

print(product_price)
        
    

