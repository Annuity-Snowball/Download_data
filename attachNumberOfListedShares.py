import pandas as pd

# Load Financial Statements file(BS), f'{year}'.csv file( # of Listed Shares )
years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']

finBS = pd.read_csv("final_FS(BS).csv")
finBS['종목코드'] = finBS['종목코드'].astype('str')

dfs = []
for year in years:
    yearly_listedSharesFile = pd.read_csv(f'{year}.csv')
    yearly_listedSharesFile = yearly_listedSharesFile.drop(columns='종목명', axis=1)
    finBS_year = finBS[finBS['SetDate'].str.contains(year)]
    merged_Data = pd.merge(finBS_year, yearly_listedSharesFile, on='종목코드', how='inner') # left inner join
    dfs.append(merged_Data)

bs = pd.concat(dfs, ignore_index=True)
print(bs)

bs.to_csv("financialStatements(BS).csv", index=False)

#Load Financial Statements file(PL)

finPL = pd.read_csv("final_FS(PL).csv")
finPL['종목코드'] = finPL['종목코드'].astype('str')

dfs2 = []
for year in years:
    yearly_listedSharesFile = pd.read_csv(f'{year}.csv')
    yearly_listedSharesFile = yearly_listedSharesFile.drop(columns='종목명', axis=1)
    finPL_year = finPL[finPL['SetDate'].str.contains(year)]
    merged_Data = pd.merge(finPL_year, yearly_listedSharesFile, on='종목코드', how='inner') # left inner join
    dfs2.append(merged_Data)

pl = pd.concat(dfs2, ignore_index=True)
pl.to_csv("financialStatements(PL).csv", index=False)