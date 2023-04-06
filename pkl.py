# Convert str -> float, Exp notation -> Real number notation
import pandas as pd
import csv

# Load
finBS = pd.read_csv("financial_BS.csv")

df = pd.read_csv("final_BS.csv") # Convert file type (BS)
df['Assets'] = df['Assets'].str.replace(',', '').astype(float)
df['Liabilities'] = df['Liabilities'].str.replace(',','').astype(float) # str -> float
df.to_csv('final_BS.csv', index=False)

df = pd.read_csv("final_PL.csv") # Convert file type (PL)
df['Revenue'] = df['Revenue'].str.replace(',', '').astype(float)
df['ProfitLoss'] = df['ProfitLoss'].str.replace(',', '').astype(float)
df['OperatingIncomeLoss'] = df['OperatingIncomeLoss'].str.replace(',', '').astype(float) # str -> float
df.to_csv('final_PL.csv', index=False)

with open("financial_PL.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i, val in enumerate(row):
            if 'e' in val or 'E' in val: # Check Exp notation
                try:
                    num_float = float(val) # Convert Exp. -> real number
                    row[i] = num_float
                except ValueError: # not Exp notation
                    pass

# Check the result
finBS = pd.read_csv("final_BS.csv")
print(finBS['Assets'].dtypes, finBS['Liabilities'].dtypes)

finPL = pd.read_csv("final_PL.csv")
print(finPL['Revenue'].dtype, finPL['ProfitLoss'].dtypes, finPL['OperatingIncomeLoss'].dtypes)