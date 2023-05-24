import winsound
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib import pyplot as plt
from datetime import datetime
import itertools
import time
from statistics import mean




df['barsize'] = df.High - df.Low
df['OnlyDate'] = pd.to_datetime(df['Date']).dt.date



max_list=[]
strg = "2017-07-20-14-00"
dt = datetime.strptime(strg, '%Y-%m-%d-%H-%M')
tme = dt.time()
df['OnlyTime'] = pd.to_datetime(df['Date']).dt.time
df['mid'] = (df.High + df.Low) / 2


for i in df.index:
        signal = 0
        try:
            if (df.Volume[i] > 50000) & (df.Close[i] > 1):
                if (df.Close[i] > df.Open[i]) & (signal == 0)\
                    & (df['OnlyTime'][i] < tme)\
                    & (df.OnlyDate[i] == df.OnlyDate[i-5]):
                    breaking = 0
                    bollinger_max = []
                    for b in range(i-10, i + 1):
                        if (df.OnlyDate[b] == df.OnlyDate[i]) & (df.Close[b] / df.Low[b] > 1.10):
                            for c in range(b, i + 0):
                                if (df.mid[c] < df.High[b]) & (df.OnlyDate[c] == df.OnlyDate[i])\
                                    & (df.mid[c] > df.mid[b]):
                                    if (i-b > 2) & (i-b < 8):
                                        prev_low = df.Low[b+1]
                                        for k in range(b+1, i + 0):
                                            if df.Low[k] > prev_low:
                                                pass
                                            if df.Low[k] < prev_low:
                                                prev_low = df.Low[k]
                                            if (k == i-1):
                                                if (df.Close[i] > df.High[b]) & (df.Volume[b] > 200000):
                                                    entry_price = df.Close[i]
                                                    entry_date = df.Date[i]
                                                    if entry_price / prev_low > 1.02:
                                                        if (signal == 0):
                                                            if (pos == 0):
                                                                sp = entry_price
                                                                pos = 1
                                                                date_plot.clear(); close_plot.clear(); open_plot.clear(); high_plot.clear()
                                                                low_plot.clear(); volume_plot.clear()
                                                                for n in range(i - 60, i + 60):
                                                                    date_plot.append(df['Date'][n]); close_plot.append(df['Close'][n])
                                                                    open_plot.append(df['Open'][n]); high_plot.append(df['High'][n])
                                                                    low_plot.append(df['Low'][n]); volume_plot.append(df['Volume'][n])
                                                                ticker = df['Symbol'][i]

                                                                R = entry_price - prev_low
                                                                stl = entry_price + 2 * R
                                                                target = entry_price - 1 * R

                                                                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, subplot_titles=(ticker, 'Volume'), row_width=[0.2, 0.7])
                                                                fig.add_trace(go.Candlestick(x=date_plot, open=open_plot, high=high_plot, low=low_plot, close=close_plot, name=ticker), row=1, col=1)


                                                                fig.add_hline(y=entry_price, line_width=1, line_dash="solid", line_color="black")
                                                                fig.add_hline(y=stl, line_width=1, line_dash="dash", line_color="red")
                                                                fig.add_hline(y=target, line_width=1, line_dash="dash", line_color="green")
                                                                fig.add_vline(x=entry_date, line_width=1, line_dash="dash", line_color="black")
                                                                b_date = df.Date[b]
                                                                fig.add_vline(x=b_date, line_width=1,
                                                                              line_dash="dash", line_color="grey")
                                                                fig.add_trace(go.Bar(x=date_plot, y=volume_plot, showlegend=False), row=2, col=1)
                                                                fig.update(layout_xaxis_rangeslider_visible=False)
                                                                print("ENTRY = " + str(sp))
                                                                print(df['Symbol'][i] + ' - ' + df['Date'][i])
                                                                shares = (balance * risk) / (sp - target)
                                                                commission = shares * 0.01
                                                                slippage = sp * shares * 0.005
                                                                

        except KeyError:
            pass


