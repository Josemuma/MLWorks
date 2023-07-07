import numpy as np
def f(x):
    return 2 + 1 / 2 * x
x = np.arange(-4, 5)
x
y = f(x)
y

# function example
x
y
beta = np.cov(x, y, ddof=0)[0, 1] / x.var()
alpha = y.mean() - beta * x.mean()
y_ = alpha + beta * x
np.allclose(y_, y) #Checks if values are numerically equal

# Data Availability
## Structured 
import eikon as ek
import configparser
c = configparser.ConfigParser()
ek.set_app_key('f00927c3b28845fd8ec05e6363e484c2e7215b4f')
c.read('../../../data/aiif.cfg')  # adjust path
# f00927c3b28845fd8ec05e6363e484c2e7215b4f
# ek.set_app_key(c['eikon']['app_id'])

symbols = ['AAPL.O', 'MSFT.O', 'NFLX.O', 'AMZN.O']
data = ek.get_timeseries(symbols,
                         fields='CLOSE',
                         start_date='2019-07-01',
                         end_date='2020-07-01')
data.info()
data.tail()

### One minute info
data = ek.get_timeseries('AAPL.O',
                         fields='*',
                         start_date='2020-08-24',
                         end_date='2020-08-25',
                         interval='minute')
data.info()
data.head()

### Fundamental
data_grid, err = ek.get_data(['AAPL.O', 'IBM', 'GOOG.O', 'AMZN.O'],
                             ['TR.TotalReturnYTD', 'TR.WACCBeta',
                              'YRHIGH', 'YRLOW',
                              'TR.Ebitda', 'TR.GrossProfit'])
data_grid

## Structured Streaming
# #pip install --upgrade git+https://github.com/yhilpisch/tpqoa.git
# import tpqoa
# oa = tpqoa.tpqoa('../../../data/pyalgo.cfg')
# oa.stream_data('BTC_USD', stop=5)

data = ek.get_timeseries('AAPL.O',
                         #fields='*',
                         start_date='2020-09-25T15:00:00',
                         end_date='2020-09-25T16:00:00',
                         interval='tick')
data.info()
data.head(8)

# Unstructured Data
news = ek.get_news_headlines('R:TSLA.O PRODUCTION', 
                              #count = 7 )
                              date_from="2020-06-01T00:00:00",
                              date_to="2020-08-01T00:00:00",
                              count=7)
news['text'][6]
storyId = news['storyId'][6] # One from which to retrieve full text
from IPython.display import HTML
HTML(ek.get_news_story(storyId)[:6])



## Unstructured Stream Data
import nlp
import requests
sources = [
    'https://nr.apple.com/dE0b1T5G3u',  # iPad Pro
    'https://nr.apple.com/dE4c7T6g1K',  # MacBook Air
    'https://nr.apple.com/dE4q4r8A2A',  # Mac Mini
]
html = [requests.get(url).text for url in sources]
###
import re
def remove_non_ascii(s):
  return ''.join(i for i in s if ord(i) < 128)

def clean_up_html(t):
  t = cleaner.clean_html(t) 
  t = re.sub('[\n\t\r]', ' ', t) 
  t = re.sub(' +', ' ', t) 
  t = re.sub('<.*?>', '', t) 
  t = remove_non_ascii(t) 
  return t
def clean_up_text(t, numbers=False, punctuation=False):
  try:
    t = clean_up_html(t) 
  except:
    pass 
  t = t.lower() 
  t = re.sub(r"what's", "what is ", t) 
  t = t.replace('(ap)', '') 
  t = re.sub(r"\'ve", " have ", t) 
  t = re.sub(r"can't", "cannot ", t) 
  t = re.sub(r"n't", " not ", t) 
  t = re.sub(r"i'm", "i am ", t) 
  t = re.sub(r"\'s", "", t) 
  t = re.sub(r"\'re", " are ", t) 
  t = re.sub(r"\'d", " would ", t) 
  t = re.sub(r"\'ll", " will ", t)
  t = re.sub(r'\s+', ' ', t) 
  t = re.sub(r"\\", "", t) 
  t = re.sub(r"\'", "", t) 
  t = re.sub(r"\"", "", t) 
  if numbers:
    t = re.sub('[^a-zA-Z ?!]+', '', t) 
  if punctuation:
    t = re.sub(r'\W+', ' ', t) 
  t = remove_non_ascii(t) 
  t = t.strip() 
  return t
###
data = [nlp.clean_up_text(t) for t in html]
data[0][0:1001]

