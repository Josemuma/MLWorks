Sharpe ratio Ratio of the mean and standard deviation of the excess returns (annualized)
Mean notional exposure Mean daily exposure
Turnover notional exposure Mean absolute daily exposure change, annualized, and 
divided by twice the mean exposure (to count round-trip trades)
Vol of vol Standard deviation of the rolling one-year standard deviation of 21-weekday or 30–calendar day overlapping returns
Mean shortfall (left tail) Mean of returns below the pth percentile (p = 1 and 5 will be considered)
Mean exceedance (right tail) Mean of returns above the pth percentile (p = 95 and 99 will be considered)

library(pacman)
p_load(quantmod, PerformanceAnalytics, cvar)
getSymbols("FDX", from = "2015-01-01", to = Sys.Date())

price = FDX$FDX.Adjusted
price = as.numeric(price)
ret = diff(log(price))
mu = mean(ret)
sigma = sd(ret)

sprintf("Mean is: %f", mu )

sprintf("standard deviation is: %f",sigma)

#Given a time series we can generate a histogram and mark the quantile value that 
#corresponds to the 95% confidence level. The quantile value in this case is the 
#critical value for which 95% of the data is on the right (higher) of the critical 
#value as represented by the histogram. The remaining 5% will be on the left. To 
#find the quantile value you will need to use the function quantile() with the proper 
#arguments. For example quantile(xts,probs=0.01) applies to a time series xts and return 
#the critical value correspondng to 99% confidence level.

hist(ret, main = "Historical FDX Log Returns", breaks = 50)
q = quantile(ret, probs = 0.05)
abline(v = q, col = "blue")

#Then calculate a VaR value for a given investment and a time horizon. Assume $2000 investment in the stock, 
#calculate the 95% VaR for 5 days’ time horizon.
#As calculated we got VaR(with log return) for 5 day time horizon and $2,000 investment = 59.227379 
#In practical terms, this means there is a 5% chance of losing at least $59.227379 over a 5 day time horizon
#VaR(with Simple return) for 5 day time horizon and $2,000 investment = 59.360998 In practical terms, 
#this means there is a 5% chance of losing at least $59.360998 over a 5 day time horizon
#Since log returns are continuously compounded returns, it is normal to see that the log returns var are lower than simple returns.

T = 5
alpha = 0.05
V = 2000
VaR = V * (exp(quantile(ret, probs = 0.05))-1)

sprintf("Var(value at risk ) is: %f", VaR )
#How does the VaR calculation change if we assume simple returns instead of the log returns

ret2 = periodReturn(FDX, period = "daily", type = "arithmetic")
mu2 = mean(ret2)
sigma2 = sd(ret2)

hist(ret2, main = "FDX Simple Returns", breaks = 50)
q = quantile(ret2, probs = 0.05)
abline(v=q, col = "red")


T = 5
alpha = 0.05
V = 2000
VarSim = V*quantile(ret2, probs=0.05)
VarSim

sprintf("Var(value at risk ) with simple returns is: %f", VarSim )


## 2 ####
# VaR Calculations: Multiple Equity portfolio var test
# Consider the times series of the three stocks DIS, TWTR, and NFLX for the 
# time-period from Jan 1,2018 to present. Assume an investment of $100,000 
# equally distributed among all three stocks.

# To calculate the portfolio VaR we will follow the methodolgy described by the
# variance-covariance. First the covariance matrix needs to be computed. We then 
# calculate the variance or volatility of the portolio as expressed in the 
# varaince-covariance method taking into the weights associated with each asset in 
# the portfolio. Finally we compute the mean or expected return of the portfolio 
# taking also into account the weights. Given the expected return and volatility 
# we should be able to compute the VaR of the portfolio. The assumption is we 
# have a normal distribution of log returns.

# Calculate the portfolio 99% VaR for 3 day, and 5 days for 100k invested amount.

symbols = c("AMZN","NVDA","NFLX")
getSymbols(symbols, src = "yahoo", from = "2018-01-01", to = Sys.Date())

AmznRd = as.numeric(periodReturn(AMZN$AMZN.Adjusted, period ="daily", type = "log"))
NvdaRd = as.numeric(periodReturn(NVDA$NVDA.Adjusted, period ="daily", type = "log"))
NFLXRd = as.numeric(periodReturn(NFLX$NFLX.Adjusted, period ="daily", type = "log"))
m = cbind(AmznRd, NvdaRd, NFLXRd)
cor(m)
w = rep(1/3, 3)
var_p = t(w) %*% cov(m) %*% w
mu_p = colMeans(m) %*% w 

T = 3
alpha = 0.01 
V = 100000 
Var3 = V*(exp(qnorm(alpha, mean = T*mu_p, sd= sqrt(T*var_p)))-1)
sprintf("Portfolio Var for 3 days is %f",Var3)

T = 5
alpha = 0.01 
V = 100000 
Var5 = V*(exp(qnorm(alpha, mean = T*mu_p, sd= sqrt(T*var_p)))-1)
sprintf("Portfolio Var for 5 days is %f",Var5)

## 3 ####
# Calculate the three-individual asset 99% VaR for 3 days. We need to divide by
# 3 because our portfolio of 100k investement was divided into 3 stocks
muAmzn = mean(AmznRd)
sigmaAmzn = sd(AmznRd)

T = 3
alpha = 0.01
V = 100000/3
VaRAmzn = V*(exp(qnorm(alpha, mean=T*muAmzn, sd=sqrt(T)*sigmaAmzn))-1)
sprintf("individual AMZN Var for 3 days is %f",VaRAmzn)

muAmzn = mean(AmznRd)
sigmaAmzn = sd(AmznRd)

T = 3
alpha = 0.01
V = 100000/3
VaRAmzn = V*(exp(qnorm(alpha, mean=T*muAmzn, sd=sqrt(T)*sigmaAmzn))-1)
sprintf("individual AMZN Var for 3 days is %f",VaRAmzn)

muNvda = mean(NvdaRd)
sigmaNvda = sd(NvdaRd)

T = 3
alpha = 0.01
V = 100000/3
VaRNvda = V*(exp(qnorm(alpha, mean=T*muNvda, sd=sqrt(T)*sigmaNvda))-1)
sprintf("individual NVDA Var for 3 days is %f",VaRNvda)

muNflx = mean(NFLXRd)
sigmaNflx = sd(NFLXRd)

T = 3
alpha = 0.01
V = 100000/3
VaRNflx = V*(exp(qnorm(alpha, mean=T*muNflx, sd=sqrt(T)*sigmaNflx))-1)
sprintf("individual NFLX Var for 3 days is %f",VaRNflx)

totalIndVar=VaRAmzn + VaRNvda + VaRNflx
sprintf("sum of individual AMZN,NVDA,NFLX var is %f",totalIndVar)

sprintf("Overall Portfolio Var for 3 days is %f",Var3)
