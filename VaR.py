# With simulations
#Importing all required libraries
#Created by Sanket Karve
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as web
from matplotlib.ticker import FuncFormatter
#!pip install PyPortfolioOpt
#Installing the Portfolio Optimzation Library
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from matplotlib.ticker import FuncFormatter

tickers = ['GOOGL','META','AAPL','NFLX','AMZN']
thelen = len(tickers)
price_data = []
price_data = yf.download(tickers, start="2018-06-20", end='2020-06-20')['Close']

df_stocks = price_data
df_stocks.columns=tickers
df_stocks.tail()

#Annualized Return
mu = expected_returns.mean_historical_return(df_stocks)
#Sample Variance of Portfolio
Sigma = risk_models.sample_cov(df_stocks)
#Max Sharpe Ratio - Tangent to the EF
from pypfopt import objective_functions, base_optimizer
ef = EfficientFrontier(mu, Sigma, weight_bounds=(0,1)) #weight bounds in negative allows shorting of stocks
sharpe_pfolio=ef.max_sharpe() 
#May use add objective to ensure minimum zero weighting to individual stocks
sharpe_pwt=ef.clean_weights()
print(sharpe_pwt)

#VaR Calculation
ticker_rx2 = []
#Convert Dictionary to list of asset weights from Max Sharpe Ratio Portfolio
sh_wt = list(sharpe_pwt.values())
sh_wt=np.array(sh_wt)

#Now, we will convert the stock prices of the portfolio to a cumulative return, 
#which may also be considered as the holding period returns (HPR)for this project.
for a in range(thelen):
  ticker_rx = df_stocks[[tickers[a]]].pct_change()
  ticker_rx = (ticker_rx+1).cumprod()
  ticker_rx2.append(ticker_rx[[tickers[a]]])
ticker_final = pd.concat(ticker_rx2,axis=1)
ticker_final

#Plot graph of Cumulative/HPR of all stocks
for i, col in enumerate(ticker_final.columns):
  ticker_final[col].plot()
  plt.show()

plt.title('Cumulative Returns')
plt.xticks(rotation=80)
plt.legend(ticker_final.columns)
#Saving the graph into a JPG file
plt.savefig('CR.png', bbox_inches='tight')

#Taking Latest Values of Return
pret = []
pre1 = []
price =[]
for x in range(thelen):
  pret.append(ticker_final.iloc[[-1],[x]])
  price.append((df_stocks.iloc[[-1],[x]]))
pre1 = pd.concat(pret,axis=1)
pre1 = np.array(pre1)
price = pd.concat(price,axis=1)
varsigma = pre1.std()
ex_rtn=pre1.dot(sh_wt)
print('The weighted expected portfolio return for selected time period is'+ str(ex_rtn))
#ex_rtn = (ex_rtn)**0.5-(1) #Annualizing the cumulative return (will not affect outcome)
price=price.dot(sh_wt) #Calculating weighted value
print(ex_rtn, varsigma,price)


# Monte Carlo
from scipy.stats import norm
import math
Time=1440 #No of days(steps or trading days in this case)
lt_price=[]
final_res=[]
for i in range(10000): #10000 runs of simulation
  daily_return=(np.random.normal(ex_rtn/Time,varsigma/math.sqrt(Time),Time))
  plt.plot(daily_return)
plt.axhline(np.percentile(daily_return,5), color='r', linestyle='dashed', linewidth=1)
plt.axhline(np.percentile(daily_return,95), color='g', linestyle='dashed', linewidth=1)
plt.axhline(np.mean(daily_return), color='b', linestyle='solid', linewidth=1)
plt.show()


plt.hist(daily_return,bins=15)
plt.axvline(np.percentile(daily_return,5), color='r', linestyle='dashed', linewidth=2)
plt.axvline(np.percentile(daily_return,95), color='r', linestyle='dashed', linewidth=2)
plt.show()

# Printing the exact values at both the upper limit and lower limit and assuming 
#our portfolio value to be $1000, we will calculated an estimate of the amount of 
#funds which should be kept to cover for our minimum losses.
print(np.percentile(daily_return,5),np.percentile(daily_return,95)) #VaR - Minimum loss of 5.7% at a 5% probability, also a gain can be higher than 15% with a 5 % probability
pvalue = 1000 #portfolio value
print('$Amount required to cover minimum losses for one day is ' + str(pvalue* - np.percentile(daily_return,5)))
print('Minimum Loss per day is', round(100*np.percentile(daily_return,5),2), '% with a 5% probability')


###################################################
yf.pdr_override()

ticker = 'GOOGL'
historical_data = []
historical_data = yf.download('GOOGL', start="2018-01-01", end='2021-03-10')['Close']
df = historical_data.to_frame()
historical_data.columns = ['Close']

alpha = 0.01
num_shares = 5000
on_date = '2021-03-09'
share_price = df['Close'][on_date]

# No assumption involved use the theoretical distribution
daily_return_rates = df['Close'].pct_change().dropna().sort_values().reset_index(drop=True)
xth = int(np.floor(0.01*len(daily_return_rates))) - 1
xth_smallest_rate = daily_return_rates[xth]

mean_return_rate = daily_return_rates.mean()

rel_VaR = num_shares * share_price * (mean_return_rate - xth_smallest_rate)
abs_VaR = -num_shares * share_price * xth_smallest_rate

print("The estimated relative VaR and absolute VaR of an investment of", num_shares, "shares of", ticker, "on", on_date, "with price $", round(share_price,2), "per share is $", round(rel_VaR,2), "and $", round(abs_VaR,2), "respectively.")


# Parametric VaR
import scipy.stats as stats

alpha = 0.01
num_shares = 5000
on_date = '2021-03-09'
share_price = df['Close'][on_date]

# Use z value, mean and standard deviation to calculation
# Assume return is normal distribution
Z_value = stats.norm.ppf(abs(alpha))
mean_return_rate = df['Close'].pct_change().mean()
std_return_rate = df['Close'].pct_change().std()

rel_VaR = -num_shares * share_price * Z_value * std_return_rate 
abs_VaR = -num_shares * share_price * (Z_value * std_return_rate + mean_return_rate)

print("The estimated relative VaR and absolute VaR of an investment of", num_shares, "shares of", ticker, "on", on_date, "with price $", round(share_price,2), "per share is $", round(rel_VaR,2), "and $", round(abs_VaR,2), "respectively.")

