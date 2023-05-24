import winsound
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib import pyplot as plt
from datetime import datetime
import itertools


df['OnlyDate'] = pd.to_datetime(df['Date']).dt.date
max_list=[]
strg = "2017-07-20-19-30"
dt = datetime.strptime(strg, '%Y-%m-%d-%H-%M')
tme = dt.time()
df['OnlyTime'] = pd.to_datetime(df['Date']).dt.time


for i in df.index:
        signal = 0
        try:
            if (df.Volume[i] > 250000) & (df.Close[i] > 1):
                if df.High[i] != df.Low[i]:
                    if (df.Close[i] > df.Open[i])\
                            & ((df.High[i] - df.Close[i]) / (df.High[i] - df.Low[i]) < 0.75)\
                            & (df.Close[i] > df.Close[i-1])\
                            & (df.High[i] / df.Low[i] > 1.10):
                        start_price = df.Low[i]
                        start_date = df.Date[i]
                        top_price = df.High[i]
                        top_date = df.Date[i]
                        breaking = 0
                        for j in range(i, i+30):
                            if (signal == 0):
                                if (df.High[j] > top_price) & (df.Low[j] > start_price + (top_price - start_price)*1/3)\
                                        & (breaking == 0):
                                    top_price = df.High[j]
                                    top_date = df.Date[j]
                                elif (df.High[j] < top_price) & (df.Low[j] > start_price + (top_price - start_price)*1/3)\
                                        & (breaking == 0):
                                    pass
                                elif (df.High[j] < top_price) & (df.Low[j] < start_price + (top_price - start_price)*1/3):
                                    entry_price = (df.Low[j] + df.Close[j]) / 2
                                    entry_date = df.Date[j]
                                    breaking = 1
                                    if (df.OnlyTime[j] < tme) & (df.OnlyDate[j] == df.OnlyDate[i-1])\
                                        & (j-i < 10):

        except KeyError:
            pass
