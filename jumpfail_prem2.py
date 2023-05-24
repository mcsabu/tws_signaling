import winsound
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib import pyplot as plt
from datetime import datetime
import itertools


df4 = pd.read_csv(
    r'C:\Users\Majer\PycharmProjects\pythonProject\Backtesting\MicroList\Micro_List_2Y_5m_prem_part1.csv', sep=';')
df5 = pd.read_csv(
    r'C:\Users\Majer\PycharmProjects\pythonProject\Backtesting\MicroList\Micro_List_2Y_5m_prem_part2.csv', sep=';')
df6 = pd.read_csv(
    r'C:\Users\Majer\PycharmProjects\pythonProject\Backtesting\MicroList\Micro_List_2Y_5m_prem_part3.csv', sep=';')
df7 = pd.read_csv(
    r'C:\Users\Majer\PycharmProjects\pythonProject\Backtesting\MicroList\Micro_List_2Y_5m_prem_part4.csv', sep=';')
df8 = pd.read_csv(
    r'C:\Users\Majer\PycharmProjects\pythonProject\Backtesting\MicroList\Micro_List_2Y_5m_prem_part5.csv', sep=';')
df9 = pd.read_csv(
    r'C:\Users\Majer\PycharmProjects\pythonProject\Backtesting\MicroList\Micro_List_2Y_5m_prem_part6.csv', sep=';')



df = pd.concat([df4, df5, df6, df7, df8, df9], ignore_index=True)


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
strg = "2017-07-20-14-00"

dt = datetime.strptime(strg, '%Y-%m-%d-%H-%M')
tme = dt.time()
df['OnlyTime'] = pd.to_datetime(df['Date']).dt.time

balance, risk = 10000, 0.02

cutoff_index = -1


for i in df.index:
    if i > cutoff_index:
        signal = 0
        try:
            if (df.Volume[i] > 50000) & (df.Close[i] > 0.75) & (df.Volume[i-1] < 50000):
                if df.High[i] != df.Low[i]:
                    if (df.Close[i] > df.Open[i])\
                            & ((df.High[i] - df.Close[i]) / (df.High[i] - df.Low[i]) < 0.90)\
                            & (df.Close[i] > df.Close[i-1])\
                            & (df.High[i] / df.Low[i] > 1.20):
                        start_price = df.Low[i]
                        start_date = df.Date[i]
                        top_price = df.High[i]
                        top_date = df.Date[i]
                        breaking = 0
                        for j in range(i, i+30):
                            if (signal == 0):
                                if (df.High[j] > top_price) & (df.Low[j] > start_price + (top_price - start_price)*0.5)\
                                        & (breaking == 0):
                                    top_price = df.High[j]
                                    top_date = df.Date[j]
                                elif (df.High[j] < top_price) & (df.Low[j] > start_price + (top_price - start_price)*0.5)\
                                        & (breaking == 0):
                                    pass
                                elif (df.High[j] < top_price) & (df.Low[j] < start_price + (top_price - start_price)*0.5):
                                    entry_price = (df.Low[j] + df.Close[j]) / 2
                                    entry_date = df.Date[j]
                                    breaking = 1
                                    if (df.OnlyDate[j] == df.OnlyDate[i])\
                                        & (j-i < 7):
                                        if (signal == 0):
                                            if (pos == 0):
                                                bp = entry_price
                                                pos = 1
                                                date_plot.clear(); close_plot.clear(); open_plot.clear(); high_plot.clear()
                                                low_plot.clear(); volume_plot.clear()
                                                for n in range(j - 60, j + 60):
                                                    date_plot.append(df['Date'][n]); close_plot.append(df['Close'][n])
                                                    open_plot.append(df['Open'][n]); high_plot.append(df['High'][n])
                                                    low_plot.append(df['Low'][n]); volume_plot.append(df['Volume'][n])
                                                ticker = df['Symbol'][j]
                                                target = bp + (top_price - start_price)*1/3
                                                stl = start_price - (top_price - start_price)*1/8
                                                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, subplot_titles=(ticker, 'Volume'), row_width=[0.2, 0.7])
                                                fig.add_trace(go.Candlestick(x=date_plot, open=open_plot, high=high_plot, low=low_plot, close=close_plot, name=ticker), row=1, col=1)
                                                fig.add_hline(y=entry_price, line_width=1, line_dash="solid", line_color="black")
                                                fig.add_hline(y=top_price, line_width=1, line_dash="dash", line_color="pink")
                                                fig.add_hline(y=stl, line_width=1, line_dash="dash", line_color="red")
                                                fig.add_hline(y=start_price, line_width=1, line_dash="dash", line_color="pink")
                                                fig.add_hline(y=start_price + (start_price + top_price)*1/3, line_width=1, line_dash="dash", line_color="pink")
                                                #fig.add_vline(x=start_date, line_width=1, line_dash="dash", line_color="pink")
                                                fig.add_hline(y=target, line_width=1, line_dash="dash", line_color="green")
                                                #fig.add_vline(x=top_date, line_width=1, line_dash="dash", line_color="red")
                                                fig.add_vline(x=entry_date, line_width=1, line_dash="dash", line_color="black")
                                                fig.add_trace(go.Bar(x=date_plot, y=volume_plot, showlegend=False), row=2, col=1)
                                                fig.update(layout_xaxis_rangeslider_visible=False)
                                                print("ENTRY = " + str(bp))
                                                print(df['Symbol'][j] + ' - ' + df['Date'][j])
                                                shares = (balance * risk) / (bp - stl)
                                                commission = shares * 0.01
                                                slippage = sp * shares * 0.005
                                                if (pos == 1):
                                                    for m in range(j + 1, len(df['Date']) - j - 1):
                                                        if (pos == 1):
                                                            cutoff_index = m + 40
                                                            if ((df['Low'][m] < stl) & (df['High'][m] > target)):
                                                                if (signal == 0):
                                                                    pos = 0; signal = 1
                                                                    both += 1
                                                                    sp = bp
                                                                    print("BOTH!!!")
                                                                    q = 'both'; sorting_list.append(q)
                                                                    symbol_list.append(df['Symbol'][m])
                                                                    fig_plot.append(fig)
                                                            # STOPLOSS
                                                            elif (df['Low'][m] < stl):
                                                                if (signal == 0):
                                                                    pos = 0; signal = 1
                                                                    sp = stl
                                                                    print("STOP = " + str(round(sp, 2)))
                                                                    lose += 1
                                                                    R = -1; R_lose_list.append(R)
                                                                    stl_date = df.Date[m]
                                                                    q = 'lose'; sorting_list.append(q)
                                                                    symbol_list.append(df['Symbol'][m])
                                                                    loss = shares * (bp - sp)
                                                                    balance = balance - loss - commission - slippage
                                                                    sum_commission += commission
                                                                    sum_slippage += slippage
                                                                    sum_loss += loss
                                                                    print(round(balance), round(-loss), round(-commission), round(-slippage))
                                                                    trade_history.append(balance)
                                                                    fig.add_vline(x=stl_date, line_width=1, line_dash="solid", line_color="red")
                                                                    fig_plot.append(fig)
                                                            # EXIT
                                                            elif (df['High'][m] > target):
                                                                if (signal == 0):
                                                                    pos = 0; signal = 1
                                                                    sp = target
                                                                    print("SELL = " + str(sp))
                                                                    win += 1
                                                                    R = (sp - bp) / (bp - stl)
                                                                    target_date = df.Date[m]
                                                                    R_win_list.append(R)
                                                                    q = 'win'; sorting_list.append(q)
                                                                    symbol_list.append(df['Symbol'][m])
                                                                    profit = shares * (sp - bp)
                                                                    balance = balance + profit - commission
                                                                    sum_commission += commission
                                                                    sum_profit += profit
                                                                    print(round(balance), round(profit), round(-commission))
                                                                    trade_history.append(balance)
                                                                    fig.add_hline(y=target, line_width=1, line_dash="solid", line_color="green")
                                                                    fig.add_vline(x=target_date, line_width=1, line_dash="solid", line_color="green")
                                                                    fig_plot.append(fig)

        except KeyError:
            pass


Total_position = win + lose + both
print(Total_position)
w = round(win / (win + lose), 2) * 100

R_win_avg = sum(R_win_list) / len(R_win_list)
R_lose_avg = sum(R_lose_list) / len(R_lose_list)

e = ((w / 100) * R_win_avg + R_lose_avg * (1 - w / 100))

Total_Gain = Total_position * e


print('avg R_win =', R_win_avg)
print('avg R_lose =', R_lose_avg)

print(R_win_list)

winsound.PlaySound('C:\\Users\\Majer\\PycharmProjects\\pythonProject\\trading_bot\\'
                   'mixkit-interface-hint-notification-911.wav', winsound.SND_FILENAME)

print(sorting_list)
print(symbol_list)

for i in range(0, len(sorting_list)):
    try:
        if sorting_list[i] == 'lose':
            lose_plot.append(fig_plot[i])
        if sorting_list[i] == 'win':
            win_plot.append(fig_plot[i])
        if sorting_list[i] == 'both':
            both_plot.append(fig_plot[i])
    except IndexError:
        pass

'''
for i in range(0, len(win_plot)):
    win_plot[i].write_html('tmp_win' + str(i) + '.html', auto_open=True)
for i in range(0, len(lose_plot)):
    lose_plot[i].write_html('tmp_lose' + str(i) + '.html', auto_open=True)
'''
for i in range(0, len(win_plot)):
    try:
        win_plot[i].write_html('tmp_win' + str(i) + '.html', auto_open=False)
    except IndexError:
        pass
for i in range(0, len(lose_plot)):
    try:
        lose_plot[i].write_html('tmp_lose' + str(i) + '.html', auto_open=False)
    except IndexError:
        pass
for i in range(0, len(both_plot)):
    try:
        both_plot[i].write_html('tmp_both' + str(i) + '.html', auto_open=False)
    except IndexError:
        pass




plt.plot(trade_history)


print("min balance: ", round(min(trade_history)))

print('Pos =', Total_position)
print('Both =', both)
print('Win =', win)
print('Lose =', lose)
print('w =', round(w, 0), '%')
print('e =', round(e, 2))
print('Gain =', round(Total_Gain, 1))

print('commission= ' + str(round(-sum_commission)))
print('slippage= ' + str(round(-sum_slippage)))
print('loss= ' + str(round(-sum_loss)))
print('profit= ' + str(round(sum_profit)))

print('Balance =', round(balance))


plt.show()  # ezt mindig legutóljára, mert csak bezárása után folytatódik a progi.
