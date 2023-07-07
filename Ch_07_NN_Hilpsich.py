# Statistical inefficiencies in financial markets with NN

# Data 
# Intraday price series of EUR/USD
# VIX to measure volatility index of asset class FX
import os
import numpy as np
import pandas as pd
from pylab import plt, mpl
plt.style.use('seaborn') # check this later as its deprecated
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.family'] = 'serif'
pd.set_option('precision', 4)
np.set_printoptions(suppress = True, precision = 4)
os.environ['PYTHONHASHSEED'] = '0'

url = 'http://hilpisch.com/aiif_eikon_id_eur_usd.csv'
symbol = 'EUR_USD'
raw = pd.read_csv(url, index_col = 0, parse_dates= True)
raw.head()
raw.info()

data = pd.DataFrame(raw['CLOSE'].loc[:])
data.columns = [symbol]
data = data.resample('1h', label = 'right').last().ffill()
data.info()
data.plot(figsize = (10,6));
plt.show()

# Baseline Prediction 
# Create lag features
lags = 5

def add_lags(data, symbol, lags, window = 20):
  cols = []
  df = data.copy()
  df.dropna(inplace=True)
  df['r'] = np.log(df / df.shift()) 
  df['sma'] = df[symbol].rolling(window).mean() 
  df['min'] = df[symbol].rolling(window).min() 
  df['max'] = df[symbol].rolling(window).max() 
  df['mom'] = df['r'].rolling(window).mean() 
  df['vol'] = df['r'].rolling(window).std() 
  df.dropna(inplace=True) 
  df['d'] = np.where(df['r'] > 0, 1, 0) 
  features = [symbol, 'r', 'd', 'sma', 'min', 'max', 'mom', 'vol'] 
  for f in features:
    for lag in range(1, lags + 1):
      col = f'{f}_lag_{lag}'
      df[col] = df[f].shift(lag)
      cols.append(col) 
  df.dropna(inplace=True) 
  return df, cols

data, cols = add_lags(data, symbol, lags)

# Check class imbalance. Que, en casos binarios, una clase no sea muchas veces 
# mas que la otra clase. Ya que en esas situaciones DNN predice a la de mayor frecuencia
# ya que estaria correcto la mayoria de veces. Por lo tanto hay que aplicar los pesos
# de manera correcta en el training step.
len(data)
c = data['d'].value_counts()
c

# Calculates appropriate weights to reach an equal weighting
def cw(df):
  c0, c1 = np.bincount(df['d']) 
  w0 = (1 / c0) * (len(df)) / 2 
  w1 = (1 / c1) * (len(df)) / 2 
  return {0: w0, 1: w1}

class_weight = cw(data)
class_weight

class_weight[0] * c[0]
class_weight[1] * c[1]

# Model creation DNN with Keras
import random
import tensorflow as tf 
from keras.layers import Dense 
from keras.models import Sequential 
from keras.optimizers import Adam 
from sklearn.metrics import accuracy_score 
Using TensorFlow backend.

# Python random seed, NumPy random seed, TensorFlow random seed
def set_seeds(seed=100):
  random.seed(seed) 
  np.random.seed(seed) 
  tf.random.set_seed(seed)

optimizer = Adam(lr=0.001)

def create_model(hl=1, hu=128, optimizer=optimizer): 
  model = Sequential() 
  model.add(Dense(hu, input_dim=len(cols), activation='relu')) # First layer
  for _ in range(hl):
    model.add(Dense(hu, activation='relu')) # Additional layers
  model.add(Dense(1, activation='sigmoid')) # Output layer
  model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy']) # Loss function , optimizer, additional metrics
  return model

set_seeds()
model = create_model(hl =1, hu = 128)

## time
model.fit(data[cols], data['d'], epochs = 50, verbose = False, class_weight = cw(data))
model.evaluate(data[cols], data['d'])

data['p'] = np.where(model.predict(data[cols]) > 0.5, 1, 0)
data['p'].value_counts()

# The performance of the model OOS, above 60%...
split=int(len(data)*0.8)
train = data.iloc[:split].copy()
test = data.iloc[split:].copy()
set_seeds()
model = create_model(hl=1, hu=128)
%%time
hist = model.fit(train[cols], train['d'],
          epochs=50, verbose=False,
          validation_split=0.2, shuffle=False,
          class_weight=cw(train))

# Evaluate IS performance
model.evaluate(train[cols], train['d'])
# Evaluate OOS performance
model.evaluate(test[cols], test['d'])
test['p'] = np.where(model.predict(test[cols]) > 0.5, 1, 0)
test['p'].value_counts()

res = pd.DataFrame(hist.history)
res[['accuracy', 'val_accuracy']].plot(figsize=(10, 6), style='--');
plt.show()


# 3 Normalization
# Previously we took laggeed features as they are. NOw we normalised (Gaussian normalization)
# Mean and SD of training features
mu, std = train.mean(), train.std()
# Normalise training data
train_ = (train - mu) / std 
set_seeds()
model = create_model(hl=2, hu=128)

##time
hist = model.fit(train_[cols], train['d'], epochs=50, 
          verbose=False, validation_split=0.2, 
          shuffle=False, class_weight=cw(train)) 

# IS Performance          
model.evaluate(train_[cols], train['d'])
# Normalise test set
test_ = (test - mu) / std

# Evalute OOS Performance
model.evaluate(test_[cols], test['d'])
test['p'] = np.where(model.predict(test_[cols]) > 0.5, 1, 0)
test['p'].value_counts()

# Problem is that it might cause OVERFITTING
res = pd.DataFrame(hist.history)
res[['accuracy', 'val_accuracy']].plot(figsize=(10, 6), style='--');
plt.show() # Shows improve training with decrease validation accuracy

# TRY: dropout, regularization, bagging
## DROPOUT
# Que NN no use todas las hidden units durante el training stage. La idea 
# es que, como una persona, olvida cosas que aprendio. Las conexiones deben
# no ser muy fuertes. 
# Un modelo de KERAS tiene layers adicionales que ayudan a manejar DROPOUT
# El parametro importante es el rate con el que las hidden units get dropped.
# Los drops pueden ser random o definidos con el seed parametro. 
from keras.layers import Dropout
def create_model(hl=1, hu=128, dropout=True, rate=0.3,
                 optimizer=optimizer):
    model = Sequential()
    model.add(Dense(hu, input_dim=len(cols),
                    activation='relu'))
    if dropout:
        model.add(Dropout(rate, seed=100)) #Adds dropout after each layer
    for _ in range(hl): 
        model.add(Dense(hu, activation='relu'))
        if dropout:
            model.add(Dropout(rate, seed=100)) #Adds dropout after each layer
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=optimizer,
                 metrics=['accuracy'])
    return model
set_seeds()
model = create_model(hl=1, hu=128, rate=0.3)
# %%time 
hist = model.fit(train_[cols], train['d'],
          epochs=50, verbose=False,
          validation_split=0.15, shuffle=False,
          class_weight=cw(train))

model.evaluate(train_[cols], train['d'])
model.evaluate(test_[cols], test['d'])
res = pd.DataFrame(hist.history)
res[['accuracy', 'val_accuracy']].plot(figsize=(10, 6), style='--');
# el drift entre uno y otro toma mas tiempo
plt.show()


## REGULARIZATION
# Grandes pesos en el NN son penalizados al calcular la Loss Function.
# Evitar conexiones fuertes y dominantes. El parametro se introduce en 
# DENSE layers. De acuerdo al parametro, el training y test pueden ser 
# muy similares. En general se usan 2 regularizadores, uno en base lineal
# y otro en euclideano. 
from keras.regularizers import l1, l2
def create_model(hl=1, hu=128, dropout=False, rate=0.3, 
                 regularize=False, reg=l1(0.0005),
                 optimizer=optimizer, input_dim=len(cols)):
    if not regularize:
        reg = None
    model = Sequential()
    model.add(Dense(hu, input_dim=input_dim,
                    activity_regularizer=reg, #Add regularization to each layer
                    activation='relu'))
    if dropout:
        model.add(Dropout(rate, seed=100))
    for _ in range(hl):
        model.add(Dense(hu, activation='relu',
                        activity_regularizer=reg)) #Add regularization to each layer
        if dropout:
            model.add(Dropout(rate, seed=100))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=optimizer,
                 metrics=['accuracy'])
    return model
set_seeds()
model = create_model(hl=1, hu=128, regularize=True)
# %%time 
hist = model.fit(train_[cols], train['d'],
          epochs=50, verbose=False,
          validation_split=0.2, shuffle=False,
          class_weight=cw(train))

model.evaluate(train_[cols], train['d'])
model.evaluate(test_[cols], test['d'])

res = pd.DataFrame(hist.history)
res[['accuracy', 'val_accuracy']].plot(figsize=(10, 6), style='--');
plt.show()

# Dropout and regularization can be used together. 
set_seeds()
model = create_model(hl=2, hu=128,
                     dropout=True, rate=0.3, #Dropout added
                     regularize=True, reg=l2(0.001),  #Regularisation added
                    )
# %%time 
hist = model.fit(train_[cols], train['d'],
          epochs=50, verbose=False,
          validation_split=0.2, shuffle=False,
          class_weight=cw(train))

model.evaluate(train_[cols], train['d'])
model.evaluate(test_[cols], test['d'])

res = pd.DataFrame(hist.history)
res[['accuracy', 'val_accuracy']].plot(figsize=(10, 6), style='--');
res.mean()['accuracy'] - res.mean()['val_accuracy']
plt.show()

## BAGGING
# Una combinacion de Keras DNN basado en el BaggingClassifier de scikit-learn.
# El resultado es guiado por el imbalance de las clases, de esta particular 
# muestra.
from sklearn.ensemble import BaggingClassifier
# from keras.wrappers.scikit_learn import KerasClassifier
from scikeras.wrappers import KerasClassifier
len(cols)
max_features = 0.75
set_seeds()
base_estimator = KerasClassifier(model=create_model,
                        verbose=False, epochs=20, hl=1, hu=128,
                        dropout=True, regularize=False,
                        input_dim=int(len(cols) * max_features)) #Base estimator, here Keras Sequential initiated

model_bag = BaggingClassifier(base_estimator=base_estimator,
                          n_estimators=15,
                          max_samples=0.75,
                          max_features=max_features,
                          bootstrap=True,
                          bootstrap_features=True,
                          n_jobs=1,
                          random_state=100,
                         ) #BaggingClassifier model is instantieated for a # of equal base estimators
# %time
model_bag.fit(train_[cols], train['d'])
model_bag.score(train_[cols], train['d'])
model_bag.score(test_[cols], test['d'])
test['p'] = model_bag.predict(test_[cols])
test['p'].value_counts()



## OPTIMIZERS
import time
optimizers = ['sgd', 'rmsprop', 'adagrad', 'adadelta',
              'adam', 'adamax', 'nadam']
# %%time
for optimizer in optimizers:
    set_seeds()
    model = create_model(hl=1, hu=128,
                     dropout=True, rate=0.3,
                     regularize=False, reg=l2(0.001),
                     optimizer=optimizer
                    ) #Instatiates the DNN model for the given optimiser
    t0 = time.time()
    model.fit(train_[cols], train['d'],
              epochs=50, verbose=False,
              validation_split=0.2, shuffle=False,
              class_weight=cw(train)) #Fit model with given optimiser
    t1 = time.time()
    t = t1 - t0
    acc_tr = model.evaluate(train_[cols], train['d'], verbose=False)[1] #Evaluates IS performance 
    acc_te = model.evaluate(test_[cols], test['d'], verbose=False)[1] #Evaluates OOS performance
    out = f'{optimizer:10s} | time[s]: {t:.4f} | in-sample={acc_tr:.4f}'
    out += f' | out-of-sample={acc_te:.4f}'
    print(out)

test['p'] = np.where(model.predict(test_[cols]) > 0.5, 1, 0)
test['p'].value_counts()

accuracy_score(test['p'], test['d'])
























