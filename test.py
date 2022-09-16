# 2016년 1분기 재무상태표저장
'''
df_base[df_base['종목코드']=='036260']
df_2016_1Q_BS.loc['036260']['ifrs_CurrentAssets'] = 27741959839
df_2016_1Q_BS.loc['036260']['ifrs_CurrentLiabilities'] = 17355581985
'''

# 2016년 2분기 재무상태표저장
'''          
df_base[df_base['종목코드']=='036260']
df_2016_2Q_BS.loc['036260']['ifrs_CurrentAssets'] = 26949283058
df_2016_2Q_BS.loc['036260']['ifrs_CurrentLiabilities'] = 12126976146
'''

# 2016년 3분기 재무상태표저장
'''
df_base[df_base['종목코드']=='036260']
df_2016_3Q_BS.loc['036260']['ifrs_CurrentAssets'] = 21981347310
df_2016_3Q_BS.loc['036260']['ifrs_CurrentLiabilities'] = 9063062098
'''

# 2016년 4분기 재무상태표저장
'''
df_base[df_base['종목코드']=='036260']
df_2016_4Q_BS.loc['036260']['ifrs_CurrentAssets'] = 24215971739
df_2016_4Q_BS.loc['036260']['ifrs_CurrentLiabilities'] = 6835915654

'''

real_portfolio_account = {'2020-01-02': 1000000.0, '2020-01-03': 1084857.0, '2020-01-06': 1112886.0, '2020-01-07': 1073335.0, '2020-01-08': 1095511.0, '2020-01-09': 1066335.0, '2020-01-10': 1214549.0, '2020-01-13': 1035767.0, '2020-01-14': 996590.0, '2020-01-15': 995886.0, '2020-01-16': 1091930.0, '2020-01-17': 953594.0, '2020-01-20': 1076332.0, '2020-01-21': 853594.0, '2020-01-22': 1103614.0, '2020-01-23': 995810.0, '2020-01-28': 1030037.0, '2020-01-29': 1178249.0, '2020-01-30': 1132974.0, '2020-01-31': 1150342.0, '2020-02-03': 1707516.0, '2020-02-04': 1717542.0, '2020-02-05': 1598419.0, '2020-02-06': 1556958.0, '2020-02-07': 1752117.0, '2020-02-10': 1578963.0, '2020-02-11': 1550351.0, '2020-02-12': 1402428.0, '2020-02-13': 1638759.0, '2020-02-14': 1668205.0, '2020-02-17': 1380301.0, '2020-02-18': 1646733.0, '2020-02-19': 1611243.0, '2020-02-20': 1486234.0, '2020-02-21': 1592605.0, '2020-02-24': 1487701.0, '2020-02-25': 1229660.0, '2020-02-26': 1439640.0, '2020-02-27': 1662007.0, '2020-02-28': 1433545.0, '2020-03-02': 2098338.0, '2020-03-03': 2036651.0, '2020-03-04': 1739071.0, '2020-03-05': 2075277.0, '2020-03-06': 2115119.0, '2020-03-09': 2073672.0, '2020-03-10': 1719805.0, '2020-03-11': 2241268.0, '2020-03-12': 2176451.0, '2020-03-13': 2308126.0, '2020-03-16': 2088967.0, '2020-03-17': 1920055.0, '2020-03-18': 2067868.0, '2020-03-19': 2300216.0, '2020-03-20': 1934926.0, '2020-03-23': 1954825.0, '2020-03-24': 2381138.0, '2020-03-25': 2486455.0, '2020-03-26': 1984225.0, '2020-03-27': 2201030.0, '2020-03-30': 1961189.0, '2020-03-31': 2130836.0, '2020-04-01': 2630835.0, '2020-04-02': 2866307.0, '2020-04-03': 2746908.0, '2020-04-06': 2519362.0, '2020-04-07': 2447943.0, '2020-04-08': 2752478.0, '2020-04-09': 3140109.0, '2020-04-10': 2625241.0, '2020-04-13': 2619421.0, '2020-04-14': 2929484.0, '2020-04-16': 2947966.0, '2020-04-17': 3230063.0, '2020-04-20': 2947982.0, '2020-04-21': 2597812.0, '2020-04-22': 3222738.0, '2020-04-23': 2838693.0, '2020-04-24': 2884845.0, '2020-04-27': 2804201.0, '2020-04-28': 2528824.0, '2020-04-29': 2663447.0, '2020-05-04': 3265332.0, '2020-05-06': 3561894.0, '2020-05-07': 3349892.0, '2020-05-08': 3154992.0, '2020-05-11': 3117888.0, '2020-05-12': 3248682.0, '2020-05-13': 3643630.0, '2020-05-14': 3298872.0, '2020-05-15': 3368778.0, '2020-05-18': 3147618.0, '2020-05-19': 2957766.0, '2020-05-20': 2921044.0, '2020-05-21': 3434534.0, '2020-05-22': 2915614.0, '2020-05-25': 3194406.0, '2020-05-26': 2919550.0, '2020-05-27': 3084944.0, '2020-05-28': 3472746.0, '2020-05-29': 3459934.0, '2020-06-01': 4234662.0, '2020-06-02': 3570540.0, '2020-06-03': 3998466.0, '2020-06-04': 4307449.0, '2020-06-05': 3900067.0, '2020-06-08': 3347737.0, '2020-06-09': 3991037.0, '2020-06-10': 3664077.0, '2020-06-11': 4269264.0, '2020-06-12': 3403682.0, '2020-06-15': 4239198.0, '2020-06-16': 3456169.0, '2020-06-17': 3944308.0, '2020-06-18': 3818354.0, '2020-06-19': 3764217.0, '2020-06-22': 3495238.0, '2020-06-23': 3316322.0, '2020-06-24': 4059224.0, '2020-06-25': 3125178.0, '2020-06-26': 3984110.0, '2020-06-29': 4107606.0, '2020-06-30': 3332387.0, '2020-07-01': 3832385.0, '2020-07-02': 4390202.0, '2020-07-03': 4450005.0, '2020-07-06': 4331083.0, '2020-07-07': 4473669.0, '2020-07-08': 3593808.0, '2020-07-09': 4734951.0, '2020-07-10': 4395348.0, '2020-07-13': 3837733.0, '2020-07-14': 4748803.0, '2020-07-15': 4824585.0, '2020-07-16': 4716874.0, '2020-07-17': 5219423.0, '2020-07-20': 4719355.0, '2020-07-21': 4247424.0, '2020-07-22': 4943353.0, '2020-07-23': 4475238.0, '2020-07-24': 5070813.0, '2020-07-27': 5163225.0, '2020-07-28': 3987836.0, '2020-07-29': 4105264.0, '2020-07-30': 4008446.0, '2020-07-31': 4007092.0}

input_money_to_portfolio = {'2020-01-02': 500000, '2020-01-03': 500000, '2020-01-06': 500000, '2020-01-07': 500000, '2020-01-08': 500000, '2020-01-09': 500000, '2020-01-10': 500000, '2020-01-13': 500000, '2020-01-14': 500000, '2020-01-15': 500000, '2020-01-16': 500000, '2020-01-17': 500000, '2020-01-20': 500000, '2020-01-21': 500000, '2020-01-22': 500000, '2020-01-23': 500000, '2020-01-28': 500000, '2020-01-29': 500000, '2020-01-30': 500000, '2020-01-31': 500000, '2020-02-03': 1000000, '2020-02-04': 1000000, '2020-02-05': 1000000, '2020-02-06': 1000000, '2020-02-07': 1000000, '2020-02-10': 1000000, '2020-02-11': 1000000, '2020-02-12': 1000000, '2020-02-13': 1000000, '2020-02-14': 1000000, '2020-02-17': 1000000, '2020-02-18': 1000000, '2020-02-19': 1000000, '2020-02-20': 1000000, '2020-02-21': 1000000, '2020-02-24': 1000000, '2020-02-25': 1000000, '2020-02-26': 1000000, '2020-02-27': 1000000, '2020-02-28': 1000000, '2020-03-02': 1500000, '2020-03-03': 1500000, '2020-03-04': 1500000, '2020-03-05': 1500000, '2020-03-06': 1500000, '2020-03-09': 1500000, '2020-03-10': 1500000, '2020-03-11': 1500000, '2020-03-12': 1500000, '2020-03-13': 1500000, '2020-03-16': 1500000, '2020-03-17': 1500000, '2020-03-18': 1500000, '2020-03-19': 1500000, '2020-03-20': 1500000, '2020-03-23': 1500000, '2020-03-24': 1500000, '2020-03-25': 1500000, '2020-03-26': 1500000, '2020-03-27': 1500000, '2020-03-30': 1500000, '2020-03-31': 1500000, '2020-04-01': 2000000, '2020-04-02': 2000000, '2020-04-03': 2000000, '2020-04-06': 2000000, '2020-04-07': 2000000, '2020-04-08': 2000000, '2020-04-09': 2000000, '2020-04-10': 2000000, '2020-04-13': 2000000, '2020-04-14': 2000000, '2020-04-16': 2000000, '2020-04-17': 2000000, '2020-04-20': 2000000, '2020-04-21': 2000000, '2020-04-22': 2000000, '2020-04-23': 2000000, '2020-04-24': 2000000, '2020-04-27': 2000000, '2020-04-28': 2000000, '2020-04-29': 2000000, '2020-05-04': 2500000, '2020-05-06': 2500000, '2020-05-07': 2500000, '2020-05-08': 2500000, '2020-05-11': 2500000, '2020-05-12': 2500000, '2020-05-13': 2500000, '2020-05-14': 2500000, '2020-05-15': 2500000, '2020-05-18': 2500000, '2020-05-19': 2500000, '2020-05-20': 2500000, '2020-05-21': 2500000, '2020-05-22': 2500000, '2020-05-25': 2500000, '2020-05-26': 2500000, '2020-05-27': 2500000, '2020-05-28': 2500000, '2020-05-29': 2500000, '2020-06-01': 3000000, '2020-06-02': 3000000, '2020-06-03': 3000000, '2020-06-04': 3000000, '2020-06-05': 3000000, '2020-06-08': 3000000, '2020-06-09': 3000000, '2020-06-10': 3000000, '2020-06-11': 3000000, '2020-06-12': 3000000, '2020-06-15': 3000000, '2020-06-16': 3000000, '2020-06-17': 3000000, '2020-06-18': 3000000, '2020-06-19': 3000000, '2020-06-22': 3000000, '2020-06-23': 3000000, '2020-06-24': 3000000, '2020-06-25': 3000000, '2020-06-26': 3000000, '2020-06-29': 3000000, '2020-06-30': 3000000, '2020-07-01': 3500000, '2020-07-02': 3500000, '2020-07-03': 3500000, '2020-07-06': 3500000, '2020-07-07': 3500000, '2020-07-08': 3500000, '2020-07-09': 3500000, '2020-07-10': 3500000, '2020-07-13': 3500000, '2020-07-14': 3500000, '2020-07-15': 3500000, '2020-07-16': 3500000, '2020-07-17': 3500000, '2020-07-20': 3500000, '2020-07-21': 3500000, '2020-07-22': 3500000, '2020-07-23': 3500000, '2020-07-24': 3500000, '2020-07-27': 3500000, '2020-07-28': 3500000, '2020-07-29': 3500000, '2020-07-30': 3500000, '2020-07-31': 3500000}

values = dict()


for key in input_money_to_portfolio.keys():
    values[key]=list()
    values[key].append(input_money_to_portfolio[key])
    values[key].append(real_portfolio_account[key])
    
print(values) 
