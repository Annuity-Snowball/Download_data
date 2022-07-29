total_balance_account = {'2021-01-01': 50471.0, '2021-02-01': 34086.0, '2021-03-01': 59648.0, '2021-04-01': 16578.0, }
input_balance_account = {'2021-05-01': 25124.0}

new_balance_account_key = list(input_balance_account.keys())[0]

print(list(total_balance_account.keys()))
print(list(input_balance_account.values())[0])

total_balance_account[new_balance_account_key]=total_balance_account[list(total_balance_account.keys())[-1]]+list(input_balance_account.values())[0]
print(total_balance_account)