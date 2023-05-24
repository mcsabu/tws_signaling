import winsound
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib import pyplot as plt
from datetime import datetime
import itertools



df4 = pd.read_csv(
    r'C:\Users\Majer\PycharmProjects\pythonProject\Backtesting\MicroList\Micro_List_2Y_5m_part1.csv', sep=';')
df5 = pd.read_csv(
    r'C:\Users\Majer\PycharmProjects\pythonProject\Backtesting\MicroList\Micro_List_2Y_5m_part2.csv', sep=';')


df6 = pd.read_csv(
    r'C:\Users\Majer\PycharmProjects\pythonProject\Backtesting\MicroList\Micro_List_2Y_5m_part3.csv', sep=';')
df7 = pd.read_csv(
    r'C:\Users\Majer\PycharmProjects\pythonProject\Backtesting\MicroList\Micro_List_2Y_5m_part4.csv', sep=';')






df = pd.concat([df4, df5, df6, df7], ignore_index=True)








pos, lose, win, num, both, target, stl, loss, profit, bp, sp, commission, slippage, sum_commission, sum_slippage,\
sum_profit, sum_loss, holding_days_sum, losing_holding_days_sum, winning_holding_days_sum = \
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
date_plot, close_plot, open_plot, high_plot, low_plot, volume_plot, vwap_plot, fig_plot, trade_history, sorting_list,\
symbol_list, R_lose_list, R_win_list, high_list, lose_plot, win_plot, both_plot =\
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

target_list = []
entry_list = []
stl_list = []
df['OnlyDate'] = pd.to_datetime(df['Date']).dt.date
max_list=[]
strg = "2017-07-20-18-30"
dt = datetime.strptime(strg, '%Y-%m-%d-%H-%M')
tme = dt.time()
df['OnlyTime'] = pd.to_datetime(df['Date']).dt.time



for i in df.index:

        signal = 0
        try:
            if (df.Volume[i] > 300000) & (df.Close[i] > 1):
                if df.High[i] != df.Low[i]:
                    if (df.Close[i] > df.Open[i])\
                            & ((df.High[i] - df.Close[i]) / (df.High[i] - df.Low[i]) < 0.5)\
                            & (df.Close[i] > df.Close[i-1])\
                            & (df.Close[i] / df.Low[i] > 1.15):
                        start_price = df.Low[i]
                        start_date = df.Date[i]
                        top_price = df.High[i]
                        top_date = df.Date[i]
                        for j in range(i, i+30):
                            if (signal == 0):
                                if (df.High[j] > top_price):
                                    top_price = df.High[j]
                                    top_date = df.Date[j]
                                else:
                                    for k in range(j+1, j+30):
                                        if (signal == 0) & (df.High[k] < top_price):
                                            if (df.Low[k] < (start_price + (top_price-start_price)*1/4))\
                                                & (k-j < 7) \
                                                & (j-i < 5): #ezeket átgondolni, leht távolabbi is oké
                                                for l in range(j+1, k):
                                                    if (signal == 0):
                                                        max_list.append(df.High[l])
                                                        if top_price >= max(max_list):

                                                            entry_price = (df.Low[k] + df.Close[k]) / 2
                                                            entry_date = df.Date[k]
                                                            max_list.clear()
                                                            if (df.OnlyTime[k] < tme) & (df.OnlyDate[k] == df.OnlyDate[i-1]):



        except KeyError:
            pass


