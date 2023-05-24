import winsound
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib import pyplot as plt
from datetime import datetime
import itertools
import time





target_list = []
entry_list = []
stl_list = []
df['barsize'] = df.High - df.Low
df['OnlyDate'] = pd.to_datetime(df['Date']).dt.date

def VWAP(df):
    H = df.High
    L = df.Low
    C = df.Close
    V = df.Volume
    return df.assign(VWAP=(V * ((H+L+C)/3)).cumsum() / V.cumsum())
df = df.groupby(['OnlyDate', 'Symbol'], group_keys=False).apply(VWAP)

def SMA(df):
    return df.assign(SMA=df.Close.rolling(window=10).mean())
df = df.groupby(['OnlyDate', 'Symbol'], group_keys=False).apply(SMA)

def avg_volume(df):
    return df.assign(avg_volume=df.Volume.rolling(window=5).mean())
df = df.groupby(['OnlyDate', 'Symbol'], group_keys=False).apply(avg_volume)

def stdev(df):
    return df.assign(stdev=df.Close.rolling(window=10).std())
df = df.groupby(['OnlyDate', 'Symbol'], group_keys=False).apply(stdev)

def prev_min(df):
    return df.assign(prev_min=df.Low.rolling(window=5).min())
df = df.groupby(['OnlyDate', 'Symbol'], group_keys=False).apply(prev_min)

def prev_min_far(df):
    return df.assign(prev_min_far=df.Low.rolling(window=20).min())
df = df.groupby(['OnlyDate', 'Symbol'], group_keys=False).apply(prev_min_far)

def prev_max(df):
    return df.assign(prev_max=df.High.rolling(window=10).max())
df = df.groupby(['OnlyDate', 'Symbol'], group_keys=False).apply(prev_max)

df['Lower_Bollinger'] = df['SMA'] - (2 * df['stdev']); df['Upper_Bollinger'] = df['SMA'] + (2 * df['stdev'])
df['Bollinger_diff'] = df['Upper_Bollinger'] - df['Lower_Bollinger']

def Bollinger_max(df):
    return df.assign(Bollinger_max=df.Bollinger_diff.rolling(window=25).max())
df = df.groupby(['OnlyDate', 'Symbol'], group_keys=False).apply(Bollinger_max)



param1 = 30000
param2 = 30000

param3 = 1
param4 = 2
param5 = 3
param6 = 100000


strg = "2017-07-20-19-30"
dt = datetime.strptime(strg, '%Y-%m-%d-%H-%M')
tme = dt.time()
df['OnlyTime'] = pd.to_datetime(df['Date']).dt.time
#barsize-os condition és min volatilitás (kisebb commission) és prc change to prev low

for i in df.index:
    signal = 0
    try:
        if (df['Bollinger_diff'][i] * param5 < df['Bollinger_max'][i - 3]):
            if (df.avg_volume[i-1] > param1) & (df.Volume[i] > param2) & (df.Close[i] > param3):
                if (df.Close[i] > df.Open[i]) & (signal == 0)\
                    & (df['OnlyTime'][i] < tme)\
                    & (df.OnlyDate[i] == df.OnlyDate[i-25]) \
                    & (df.High[i] > df.VWAP[i])\
                    & (df.High[i] > df.prev_max[i-1]):

                    entry_price = df.prev_max[i-1]
                    entry_date = df.Date[i]
                    prev_low = df.prev_min[i]
                    if entry_price / prev_low > 1.02:


    except KeyError:
        pass


