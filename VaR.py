import numpy as np
import pandas as pd
import seaborn as sns
sns.set(style="darkgrid")
import matplotlib.pyplot as plt

import statsmodels.api as sm
import scipy.stats as scs

import warnings
warnings.filterwarnings('ignore')

# 2
import yfinance as yf
raw = yf.download(
        tickers = "^GSPC ^VIX 000001.SS CNYUSD=X",
        start = "2007-01-01",
        end = "2020-05-01",
        interval = "1d",
        group_by = "ticker"
        )
raw.to_csv("raw.csv", header=True)
# 3
df = pd.read_csv("raw.csv")

# Data Cleanup and Preprocessing
# Leave only dates and close values.
df = df.iloc[3:, [0] + [6*i + 4 for i in range(4)]]
date = pd.to_datetime(df.iloc[:,0]).rename("date", inplace=True)
# initialize new dataframe
df = pd.DataFrame({"date": date,
                    "SPX": df["^GSPC.3"],
                    "VIX": df["^VIX.3"],
                    "SSE": df["000001.SS.3"],
                    "CNY": df["CNYUSD=X.3"]})
df.set_index(df["date"], drop=True, inplace=True)
df = df.dropna(axis=0, how="any")

# Manual correction of error entry 
# for this particular date in Yahoo Finance data.
# Replaced with data from investing.com
df.loc["2011-07-18", "CNY"] = 0.1546

# preserve date range Series for log-return dataframe.
date = df["date"]
del df["date"]

for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# generate graphs
sns.relplot(kind="line", data=df[["SPX","SSE"]])
plt.show()
sns.relplot(kind="line", data=df["VIX"])
plt.show()
sns.relplot(kind="line", data=df["CNY"])
plt.show()

# 4
# Convert daily close quotes to one-day-ahead log returns in percentages + generate graphs
def getLogReturns(quotes):
    return [100 * np.log(quotes[i] / quotes[i-1])
           for i in range(1, len(quotes))]

df_lret = pd.DataFrame(columns=df.columns, index=date[1:])
for col in df_lret.columns:
    if col == "VIX":
        df_lret[col] = df[col][1:]
    else:
        df_lret[col] = getLogReturns(df[col].tolist())
    sns.relplot(kind="line", data=df_lret[col])
    plt.show()

# 5
# Separate Dataframes for the Great Recession and Coronavirus Recession
# defined respectively as Dec 2007 ~ Jun 2009 and Dec 2019 ~

# Global Date Variables
ALL_START = "2007-01-01"
ALL_END = "2020-05-01"
# TRAIN and Forecast
TRAIN_END = "2018-12-31"
FORECAST_START = "2019-01-01"
GR_START = "2007-12-01"
GR_END = "2009-07-01"
# COVID TIME
COVID_START = "2019-12-01"
COVID_END = "2020-05-01"

COLS_EXCL_VIX = ("SPX", "SSE", "CNY")

GRdf = df[GR_START:GR_END].copy()
GRdf_lret = df_lret[GR_START:GR_END].copy()

CRdf = df[COVID_START:].copy()
CRdf_lret = df_lret[COVID_START:].copy()

resultsdb = {"ALL": ["Full Timeframe", df_lret],
             "CR": ["COVID-19 Recession", CRdf_lret]}

for data in GRdf, CRdf:
    sns.relplot(kind="line", data=data[["SPX","SSE"]])
    plt.show()
    sns.relplot(kind="line", data=data["VIX"])
    plt.show()
    sns.relplot(kind="line", data=data["CNY"])
    plt.show()

# 6
# Diagnostic Tests
# Augmented Dickey-Fuller: Stationarity (Unit Root)
def adf(timeseries, title, cutoff=0.01):
    result = False
    
    print('Results of Dickey-Fuller Test for: ' + title)
    dftest = sm.tsa.stattools.adfuller(timeseries, autolag='AIC')
    
    pvalue = dftest[1]
    if pvalue < cutoff:
        print('p-value = %.6f. The series is likely stationary.' % pvalue)
        result = True
    else:
        print('p-value = %.6f. The series is likely non-stationary.' % pvalue)

    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)
    print()
    
    return result

for v in resultsdb.values():
    data = v[1]
    print(v[0] + ": \n")
    for col in data.columns:
        title = " - ".join((v[0], col))
        adf(data[col], title)
        print()
  
