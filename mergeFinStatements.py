import pandas as pd

# 1) Merge final_BS, financial_BS -> final_FS(BS).csv

file_path = 'C:\\Users\pth99\OneDrive\Desktop\python workspace\project\\Download_data' # Set the file directory

bs1 = pd.read_csv("final_BS.csv") # Balance Sheet #1
bs2 = pd.read_csv("financial_BS.csv") # Balance Sheet #2

# finBS = pd.concat([bs1, bs2], axis=0)  # Merge(row-wise)
# print(finBS) # Check the result
# print(finBS['Assets'].dtypes, finBS['Liabilities'].dtypes) # Check the data type
# finBS.to_csv("final_FS(BS).csv", index=False) # save

# 2) Merge final_PL, financial_PL -> final_FS(PL).csv

pl1 = pd.read_csv("final_PL.csv") # Profit and loss account #1
pl2 = pd.read_csv("financial_PL.csv") # Profit and loss account #2

# finPL = pd.concat([pl1, pl2], axis=0) # Merge(row-wise)
# print(finPL) # Check the result
# print(finPL['Revenue'].dtypes, finPL['OperatingIncomeLoss'].dtypes, finPL['ProfitLoss'].dtypes) # Check the data type
# finPL.to_csv("final_FS(PL).csv", index=False) # save

# check the # of columns
# bs = pd.read_csv("final_FS(BS).csv")
# pl = pd.read_csv("final_FS(PL).csv")
#
# print(bs)
# print(pl)

