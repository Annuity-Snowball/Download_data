import pandas as pd

stock_list = [
['FR0010340141', 'ADP', '51.00', '-', '-', '-'], 
['ES0105046009', 'AENA', 'SA', '150.00', '-', '-', '-'], 
['US0255371017', 'AMERICAN', 'ELECTRIC', 'POWER', '93.00', '-', '-', '-'], 
['US0304201033', 'AMERICAN', 'WATER', 'WORKS', 'CO', 'INC', '33.00', '-', '-', '-'], 
['CNE1000001X0', 'ANHUI', 'EXPRESSWAY', 'CO', 'LTD-H', '553.00', '-', '-', '-'], 
['IT0003506190', 'ATLANTIA', 'SPA', '1,019.00', '-', '-', '-'], 
['AU0000013559', 'ATLAS', 'ARTERIA', '1,852.00', '-', '-', '-'], 
['NZAIAE0002S6', 'AUCKLAND', 'INTL', 'AIRPORT', 'LTD', '2,373.00', '-', '-', '-'], 
['CNE100000221', 'BEIJING', 'AIRPORT', '2,400.00', '-', '-', '-'], 
['US2044096012', 'CEMIG', 'SA', '274.00', '-', '-', '-'], 
['CNE100001T80', 'CGN', 'POWER', 'CO', 'LTD-H', '149.00', '-', '-', '-'], 
['US16411R2085', 'CHENIERE', 'ENERGY', 'INC', '59.00', '-', '-', '-'], 
['CNE100000HD4', 'CHINA', 'LONGYUAN', 'POWER', 'GROUP-H', '600.00', '-', '-', '-'], 
['HK0144000764', 'CHINA', 'MERCHANTS', 'HOLD', '2,000.00', '-', '-', '-'], 
['HK2380027329', 'CHINA', 'POWER', '956.00', '-', '-', '-'], 
['US2091151041', 'CONSOLIDATED', 'EDISON', 'INC', '57.00', '-', '-', '-'], 
['US21037T1097', 'CONSTELLATION', 'ENERGY', '52.00', '-', '-', '-'], 
['BMG2442N1048', 'COSCO', 'Pacific', 'Ltd', '2,600.00', '-', '-', '-'], 
['BMG2109G1033', 'China', 'Gas', 'Holdings', 'Ltd', '400.00', '-', '-', '-'], 
[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

# print(stock_list)
# result=list()
# for stock_info in stock_list:
#     if len(stock_info)>6:
#         temp=list()
#         temp.append(stock_info[0])
#         temp.append(' '.join(stock_info[1:-4]))
#         temp.append(stock_info[-4])
#         temp.append(stock_info[-3])
#         temp.append(stock_info[-2])
#         temp.append(stock_info[-1])
#         result.append(temp)
#     else:
#         result.append(stock_info)
# print(result)

a= ['1','2','3','4','5','6','7']
a[1]=" ".join(a[1:-4])
del a[2:-4]
print(a)


# df = pd.DataFrame({},columns=['종목코드','구성종목명','주식수(계약수)','평가금액','시가총액','시가총액기준구성비중'])
# df.loc[0]=stock_list[1]
# # df.loc[1]=stock_list[1]
# # for i in range(len(stock_list)):
# #     df.loc[i]=stock_list[i]
# print(stock_list[1])
# print(df)
