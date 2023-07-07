import eikon as ek
import configparser
c = configparser.ConfigParser()
ek.set_app_key('f00927c3b28845fd8ec05e6363e484c2e7215b4f')

# Mean-Variance Portfolio Theory
import numpy as np
import pandas as pd
from pylab import plt, mpl
from scipy.optimize import minimize
plt.style.use('seaborn')
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.family'] = 'serif'
np.set_printoptions(precision=5, suppress=True,
                   formatter={'float': lambda x: f'{x:6.3f}'})

url = 'http://hilpisch.com/aiif_eikon_eod_data.csv'
raw = pd.read_csv(url, index_col=0, parse_dates=True).dropna()
raw.info()

symbols = ['AAPL.O', 'MSFT.O', 'INTC.O', 'AMZN.O', 'GLD'] # which symbols to invest
rets = np.log(raw[symbols] / raw[symbols].shift(1)).dropna() #log returns
(raw[symbols[:]] / raw[symbols[:]].iloc[0]).plot(figsize=(10, 6)); 
plt.show()

# Equal weights(?)
weights = len(rets.columns) * [1 / len(rets.columns)]
weights
def port_return(rets, weights):
    return np.dot(rets.mean(), weights) * 252  # annualized
port_return(rets, weights)
def port_volatility(rets, weights):
    return np.dot(weights, np.dot(rets.cov() * 252 , weights)) ** 0.5  # annualized
port_volatility(rets, weights)
def port_sharpe(rets, weights):
    return port_return(rets, weights) / port_volatility(rets, weights)
port_sharpe(rets, weights) # No short rate

# MC Randomized portfolio, No short sales
w = np.random.random((1000, len(symbols)))
w = (w.T / w.sum(axis=1)).T
w[:5] # Pesos por row
w[:5].sum(axis=1)

pvr = [(port_volatility(rets[symbols], weights),
        port_return(rets[symbols], weights))
       for weights in w]
pvr = np.array(pvr)

psr = pvr[:, 1] / pvr[:, 0] # Sharpe ratio
plt.figure(figsize=(10, 6))
fig = plt.scatter(pvr[:, 0], pvr[:, 1],
                  c=psr, cmap='coolwarm')
cb = plt.colorbar(fig)
cb.set_label('Sharpe ratio')
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.title(' | '.join(symbols));
plt.show()

## Backtest a strategy from BOY 2011
# so that each year it is updated with most recent info 
bnds = len(symbols) * [(0, 1),]
bnds
cons = {'type': 'eq', 'fun': lambda weights: weights.sum() - 1} # Specifies that all weights need to add up to 100%
opt_weights = {}

for year in range(2010, 2019):
    rets_ = rets[symbols].loc[f'{year}-01-01':f'{year}-12-31'] # Change for each eyar
    ow = minimize(lambda weights: -port_sharpe(rets_, weights),
                  len(symbols) * [1 / len(symbols)],
                  bounds=bnds,
                  constraints=cons)['x'] # derive portfolio and maximise Sharpe ratio
    opt_weights[year] = ow
opt_weights

# To avoid having 0% of one asset, it can be defined a min % per asset and also 
# look at the statistics
# res = pd.DataFrame()
res = []
for year in range(2010, 2019):
    rets_ = rets[symbols].loc[f'{year}-01-01':f'{year}-12-31']
    epv = port_volatility(rets_, opt_weights[year]) # volatitlity
    epr = port_return(rets_, opt_weights[year]) # returns
    esr = epr / epv # Sharpe ratio
    rets_ = rets[symbols].loc[f'{year + 1}-01-01':f'{year + 1}-12-31'] # +1 year
    rpv = port_volatility(rets_, opt_weights[year])
    rpr = port_return(rets_, opt_weights[year])
    rsr = rpr / rpv
    res.append(pd.DataFrame({'epv': epv, 'epr': epr, 'esr': esr,
                                   'rpv': rpv, 'rpr': rpr, 'rsr': rsr},
                                  index=[year + 1]))
res = pd.concat(res)
res
res.mean()
res[['epv', 'rpv']].corr()
res[['epv', 'rpv']].plot(kind='bar', figsize=(10, 6),
        title='Expected vs. Realized Portfolio Volatility');
plt.show()
res[['epr', 'rpr']].corr()
res[['epr', 'rpr']].plot(kind='bar', figsize=(10, 6),
        title='Expected vs. Realized Portfolio Return');
plt.show()
res[['esr', 'rsr']].corr()
res[['esr', 'rsr']].plot(kind='bar', figsize=(10, 6),
        title='Expected vs. Realized Sharpe Ratio');
plt.show()

## Capital Asset Pricing Model
r = 0.005
market = '.SPX' # Market Portfolio
rets = np.log(raw / raw.shift(1)).dropna()

res = []
for sym in rets.columns[:4]:
    print('\n' + sym)
    print(54 * '=')
    for year in range(2010, 2019):
        rets_ = rets.loc[f'{year}-01-01':f'{year}-12-31']
        muM = rets_[market].mean() * 252
        cov = rets_.cov().loc[sym, market] # Beta of stock
        var = rets_[market].var() # Beta of stock
        beta = cov / var  # Beta of stock
        rets_ = rets.loc[f'{year + 1}-01-01':f'{year + 1}-12-31']
        muM = rets_[market].mean() * 252
        mu_capm = r + beta * (muM - r) # E[r] given previous year beta and current year market portf performance
        mu_real = rets_[sym].mean() * 252 # Calculate realized performance of stock for current year
        res.append(pd.DataFrame({'symbol': sym,
                                       'mu_capm': mu_capm,
                                       'mu_real': mu_real},
                                      index=[year + 1]))#,
                        # sort=True)
        print('{} | beta: {:.3f} | mu_capm: {:6.3f} | mu_real: {:6.3f}'
              .format(year + 1, beta, mu_capm, mu_real))
res = pd.concat(res)
res

sym = 'AMZN.O'
res[res['symbol'] == sym].corr()
res[res['symbol'] == sym].plot(kind='bar',
                figsize=(10, 6), title=sym);
plt.show()
grouped = res.groupby('symbol').mean()
grouped
grouped.plot(kind='bar', figsize=(10, 6), title='Average Values');
plt.show()

## Arbitrage-Pricing Theory
factors = ['.SPX', '.VIX', 'EUR=', 'XAU='] # Four factors
res = pd.DataFrame()
np.set_printoptions(formatter={'float': lambda x: f'{x:5.2f}'})

res = []
for sym in rets.columns[:4]:
    print('\n' + sym)
    print(71 * '=')
    for year in range(2010, 2019):
        rets_ = rets.loc[f'{year}-01-01':f'{year}-12-31']
        reg = np.linalg.lstsq(rets_[factors],
                              rets_[sym], rcond=-1)[0] # Multivariate regression
        rets_ = rets.loc[f'{year + 1}-01-01':f'{year + 1}-12-31']
        mu_apt = np.dot(rets_[factors].mean() * 252, reg) # APT-predicted return of the stock
        mu_real =  rets_[sym].mean() * 252 # Realized return of stock
        res.append(pd.DataFrame({'symbol': sym,
                        'mu_apt': mu_apt, 'mu_real': mu_real},
                         index=[year + 1]))
        print('{} | fl: {} | mu_apt: {:6.3f} | mu_real: {:6.3f}'
              .format(year + 1, reg.round(2), mu_apt, mu_real))
              
res = pd.concat(res)
res

sym = 'AMZN.O'
res[res['symbol'] == sym][['mu_apt','mu_real']].corr()
res[res['symbol'] == sym].plot(kind='bar',
                figsize=(10, 6), title=sym);
plt.show()

grouped = res.groupby('symbol').mean()
grouped
grouped.plot(kind='bar', figsize=(10, 6), title='Average Values');
plt.show()

### More risky factors
factors = pd.read_csv('http://hilpisch.com/aiif_eikon_eod_factors.csv',
                      index_col=0, parse_dates=True)
factors.info()
(factors / factors.iloc[0]).plot(figsize=(10, 6)); # Normalise and plot data
plt.show()
start = '2017-01-01'
end = '2020-01-01'
retsd = rets.loc[start:end].copy()
retsd.dropna(inplace=True)
retsf = np.log(factors / factors.shift(1))
retsf = retsf.loc[start:end]
retsf.dropna(inplace=True)
retsf = retsf.loc[retsd.index].dropna()
retsf.corr()

# New factor loadings with updated factors. First half to get the factors that are 
# applied to the second half
# res = pd.DataFrame()

np.set_printoptions(formatter={'float': lambda x: f'{x:5.2f}'})
split = int(len(retsf) * 0.5)
res = []
for sym in rets.columns[:4]:
    print('\n' + sym)
    print(74 * '=')
    retsf_, retsd_ = retsf.iloc[:split], retsd.iloc[:split]
    reg = np.linalg.lstsq(retsf_, retsd_[sym], rcond=-1)[0]   
    retsf_, retsd_ = retsf.iloc[split:], retsd.iloc[split:]
    mu_apt = np.dot(retsf_.mean() * 252, reg)
    mu_real =  retsd_[sym].mean() * 252
    res.append(pd.DataFrame({'mu_apt': mu_apt,
                    'mu_real': mu_real}, index=[sym,]))
    print('fl: {} | apt: {:.3f} | real: {:.3f}'
          .format(reg.round(1), mu_apt, mu_real))
          
res = pd.concat(res)          
res
res.plot(kind='bar', figsize=(10, 6));
plt.show()

sym
rets_sym = np.dot(retsf_, reg)
rets_sym = pd.DataFrame(rets_sym,
                        columns=[sym + '_apt'],
                        index=retsf_.index)
rets_sym[sym + '_real'] = retsd_[sym]
rets_sym.mean() * 252
rets_sym.std() * 252 ** 0.5
rets_sym.corr()
rets_sym.cumsum().apply(np.exp).plot(figsize=(10, 6));
plt.show()

rets_sym['same'] = (np.sign(rets_sym[sym + '_apt']) ==
                    np.sign(rets_sym[sym + '_real']))
rets_sym['same'].value_counts()
rets_sym['same'].value_counts()[True] / len(rets_sym)


