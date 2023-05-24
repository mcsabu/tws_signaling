import winsound
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib import pyplot as plt
from datetime import datetime


df4 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part7.csv', sep=';')
df5 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part8.csv', sep=';')

df6 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part9.csv', sep=';')

df7 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part10.csv', sep=';')

df8 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part11.csv', sep=';')

df9 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part12.csv', sep=';')



df = pd.concat([df4, df5, df6, df7, df8, df9], ignore_index=True)

df['-2_Open'] = df['Open'].shift(2)
df['-1_High'] = df['High'].shift(1); df['-2_High'] = df['High'].shift(2)
df['-1_Low'] = df['Low'].shift(1); df['-2_Low'] = df['Low'].shift(2); df['-3_Low'] = df['Low'].shift(3)
df['-4_Low'] = df['Low'].shift(4); df['-5_Low'] = df['Low'].shift(5); df['-6_Low'] = df['Low'].shift(6)
df['-7_Low'] = df['Low'].shift(7); df['-8_Low'] = df['Low'].shift(8); df['-9_Low'] = df['Low'].shift(9)
df['-10_Low'] = df['High'].shift(10); df['-11_Low'] = df['Low'].shift(11); df['-12_Low'] = df['Low'].shift(12)
df['-13_Low'] = df['Low'].shift(13); df['-14_Low'] = df['Low'].shift(14); df['-15_Low'] = df['Low'].shift(15)
df['-1_High'] = df['High'].shift(1); df['-2_High'] = df['High'].shift(2); df['-3_High'] = df['High'].shift(3)
df['-4_High'] = df['High'].shift(4); df['-5_High'] = df['High'].shift(5); df['-6_High'] = df['High'].shift(6)
df['-7_High'] = df['High'].shift(7); df['-8_High'] = df['High'].shift(8); df['-9_High'] = df['High'].shift(9)
df['-10_High'] = df['High'].shift(10); df['-11_High'] = df['High'].shift(11); df['-12_High'] = df['High'].shift(12)
df['-13_High'] = df['High'].shift(13); df['-14_High'] = df['High'].shift(14); df['-15_High'] = df['High'].shift(15)



df['Volume_1'] = df['Volume'].shift(1); df['Volume_2'] = df['Volume'].shift(2)
df['max_High'] = df[['-1_High', '-2_High', 'High']].max(axis=1)
df['min_Low'] = df[['-1_Low', '-2_Low', 'Low']].min(axis=1)
df['bar_size'] = df['max_High'] - df['min_Low']
df['max_high_open_diff'] = df['max_High'] - df['-2_Open']
df['min_low_close_diff'] = df['Close'] - df['min_Low']
df['0_15m_Volume'] = df['Volume_2'] + df['Volume_1'] + df['Volume']
df['max_Volume'] = df[['Volume_2', 'Volume_1', 'Volume']].max(axis=1)
df['min_Volume'] = df[['Volume_2', 'Volume_1', 'Volume']].min(axis=1)
df.loc[((df['Volume_2'] - df['Volume_1']) > 0) & ((df['Volume_2'] - df['Volume']) > 0), 'Volmax'] = 2
df.loc[((df['Volume_1'] - df['Volume_2']) > 0) & ((df['Volume_1'] - df['Volume']) > 0), 'Volmax'] = 1
df.loc[((df['Volume'] - df['Volume_2']) > 0) & ((df['Volume'] - df['Volume_1']) > 0), 'Volmax'] = 0
df.loc[((df['-2_Low'] - df['-1_Low']) < 0) & ((df['-2_Low'] - df['Low']) < 0), 'Lowmin'] = 2
df.loc[((df['-1_Low'] - df['-2_Low']) < 0) & ((df['-1_Low'] - df['Low']) < 0), 'Lowmin'] = 1
df.loc[((df['Low'] - df['-2_Low']) < 0) & ((df['Low'] - df['-1_Low']) < 0), 'Lowmin'] = 0
df['-1_15m_Volume'] = df['Volume'].shift(3) + df['Volume'].shift(4) + df['Volume'].shift(5)
df['-2_15m_Volume'] = df['Volume'].shift(6) + df['Volume'].shift(7) + df['Volume'].shift(8)
df['-3_15m_Volume'] = df['Volume'].shift(9) + df['Volume'].shift(10) + df['Volume'].shift(11)
df['-4_15m_Volume'] = df['Volume'].shift(12) + df['Volume'].shift(13) + df['Volume'].shift(14)
df['-5_15m_Volume'] = df['Volume'].shift(15) + df['Volume'].shift(16) + df['Volume'].shift(17)

df['-1-3_15m_Volume_mean'] = df[['-1_15m_Volume', '-2_15m_Volume', '-3_15m_Volume']].mean(axis=1)
df['-1-5_15m_Volume_min'] = df[['-1_15m_Volume', '-2_15m_Volume', '-3_15m_Volume',
                                '-4_15m_Volume', '-5_15m_Volume']].min(axis=1)
df['min_prev45m_Low'] = df[['-3_Low', '-4_Low', '-5_Low', '-6_Low', '-7_Low', '-8_Low', '-9_Low',
                            '-10_Low', '-11_Low', '-12_Low']].min(axis=1)
df['max_prev45m_High'] = df[['-3_High', '-4_High', '-5_High', '-6_High', '-7_High', '-8_High', '-9_High',
                            '-10_High', '-11_High', '-12_High', '-13_High', '-14_High', '-15_High']].max(axis=1)
df['OnlyDate'] = pd.to_datetime(df['Date']).dt.date
df['OnlyTime'] = pd.to_datetime(df['Date']).dt.time


strg = "2017-07-20-19-00"
dt = datetime.strptime(strg, '%Y-%m-%d-%H-%M')
tme = dt.time()

def VWAP(df):
    H = df.High
    L = df.Low
    C = df.Close
    V = df.Volume
    return df.assign(VWAP=(V * ((H+L+C)/3)).cumsum() / V.cumsum())
df = df.groupby(['OnlyDate', 'Symbol'], group_keys=False).apply(VWAP)


'''BULL REDWICK
VWAP felett uptrendben történik egy kis lefele menetben spring back (redwick), nagy visszahúzás, lehet
az utolsó bar-nak (green barnak) kell nagy volumeúnak lennie vagy kicsinek..?'''

R = 2.5

base1 = df['Open'] < 8
base2 = df['Open'] > 1
base3 = df['0_15m_Volume'] > 300000 #LIQUIDITY
base4 = 1
base5 = df['OnlyDate'] == df['OnlyDate'].shift(5)
base6 = df['Close'] / df['min_Low'] > 1.03 #VOLATILITY
base7 = tme > df['OnlyTime']
base8 = 1
base9 = 1
base10 = 1


'''
uptrending VWAP history; 12-vel előtte 5%al, 24-el 10%al

open legyen a high/vwap 

mivan hogyha kicsivel a minlow alá rakni a stl



df['0_15m_Volume'] < 0.8 * df['0_15m_Volume'].shift(6)
df['0_15m_Volume'] < 0.8 * df['0_15m_Volume'].shift(9)
df['-3_15m_Volume'] > 300000
df['Volmax'] != df['Lowmin']
df['max_High'] < df['max_High'].shift(3)
df['max_High'] < df['max_High'].shift(6)

opt = df['max_Volume'] < 1 * df['min_Volume'].shift(3)
'''


strat1 = df['Close'] - df['-2_Open'] < 0
strat2 = df['min_low_close_diff'] / df['bar_size'] > 0.5
strat3 = df['max_high_open_diff'] / df['bar_size'] < 0.3
strat4 = 1
strat5 = df['bar_size'] < 0.8 * df['bar_size'].shift(3)
strat6 = df['0_15m_Volume'] < 0.8 * df['0_15m_Volume'].shift(3) #ezt paraméterezni
strat7 = df['0_15m_Volume'] > 0.4 * df['0_15m_Volume'].shift(3) #ezt paraméterezni
strat8 = df['min_Low'] > 1 * df['VWAP'] #minlow
strat9 = 1
strat10 = 1


opt1 = df['VWAP'] > 1.05 * df['VWAP'].shift(24)
opt2 = 1
opt3 = (df['max_prev45m_High'] - df['VWAP']) * 0.33 < df['Close'] - df['VWAP']
opt4 = 1
opt5 = 1
opt6 = df['Close'] > df['Close'].shift(80)
opt7 = df['Close'] > df['Close'].shift(160)
opt8 = 1
opt9 = 1
opt10 = 1

#BUY condition
df['signal'] = np.where(base1 & base2 & base3 & base4 & base5 & base6 & base7 & base8 & base10 &
                        strat1 & strat2 & strat3 & strat4 & strat5 & strat6 & strat7 & strat8 & strat9 & strat10 &
                        opt1 & opt2 & opt3 & opt4 & opt5 & opt6 & opt7 & opt8 & opt9 & opt10
                        , 1, np.nan)

#TARGET
df['R'] = R * (df['Close'] - df['min_Low'])
df['target_R'] = df['Close'] + df['R']
df['result'] = 0
pos, lose, win, num, both, target, stl, loss, profit, bp, sp = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
commission, slippage = 0, 0
date_plot, close_plot, open_plot, high_plot, low_plot, volume_plot, vwap_plot, fig_plot = [], [], [], [], [], [], [], []

balance, risk = 10000, 0.02
trade_history = []
sorting_list = []
symbol_list = []

for i in df.index:

    if (df['signal'][i] == 1):
        # ENTRY
        if (pos == 0):
            bp = df["Close"][i]
            pos = 1
            for j in range(i - 60, i + 60):
                date_plot.append(df['Date'][j])
                close_plot.append(df['Close'][j])
                open_plot.append(df['Open'][j])
                high_plot.append(df['High'][j])
                low_plot.append(df['Low'][j])
                volume_plot.append(df['Volume'][j])
                vwap_plot.append(df['VWAP'][j])

            target_plot = df['target_R'][i]
            stl_plot = df['min_Low'][i]
            entry_plot = bp
            ticker = df['Symbol'][i]

            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                vertical_spacing=0.03, subplot_titles=(ticker, 'Volume'),
                                row_width=[0.2, 0.7])

            fig.add_trace(go.Candlestick(x=date_plot, open=open_plot, high=high_plot,
                                         low=low_plot, close=close_plot, name=ticker),
                                         row=1, col=1
            )
            fig.add_trace(go.Scatter(
                x=date_plot,
                y=vwap_plot,
                mode='lines',
                name='VWAP',
                line=dict(color='royalblue', width=2)
            ))
            fig.add_hline(y=entry_plot, line_width=2, line_dash="dash", line_color="black")
            fig.add_hline(y=stl_plot, line_width=2, line_dash="dash", line_color="red")
            fig.add_hline(y=target_plot, line_width=2, line_dash="dash", line_color="green")
            fig.add_vline(x=df['Date'][i], line_width=2, line_dash="dash", line_color="black")
            fig.add_trace(go.Bar(x=date_plot, y=volume_plot, showlegend=False), row=2, col=1)
            fig.update(layout_xaxis_rangeslider_visible=False)

            fig_plot.append(fig)

            stl = df['min_Low'][i]
            target = df['target_R'][i]
            print("ENTRY = " + str(bp))
            print(df['Symbol'][i] + ' - ' + df['Date'][i])

            shares = (balance * risk) / (bp - stl)
            profit = shares * (target - bp)
            loss = shares * (bp - stl)
            commission = shares * 0.01
            slippage = bp * shares * 0.005

            print(balance)
            print(shares)

    elif (pos == 1):
        date_plot.clear()
        close_plot.clear()
        open_plot.clear()
        high_plot.clear()
        low_plot.clear()
        volume_plot.clear()
        vwap_plot.clear()

        # Both case - felbontásból keletkező hiba
        if ((df['Low'][i] < stl) & (df['High'][i] > target)):
            pos = 0
            both += 1
            sp = bp
            print("BOTH!!!")
            q = 'both'
            sorting_list.append(q)
        # STOPLOSS
        elif (df['Low'][i] < stl):
            pos = 0
            sp = stl
            print("STOP = " + str(sp))
            df[df['result'][i]] = -1
            lose += 1
            q = 'lose'

            sorting_list.append(q)
            symbol_list.append(df['Symbol'][i])

            balance = balance - loss - commission - slippage
            print(balance)
            print(loss)
            print(commission)
            print(slippage)
            trade_history.append(balance)

        # EXIT
        elif (df['High'][i] > target):
            pos = 0
            sp = target
            print("SELL = " + str(sp))
            df[df['result'][i]] = 1
            win += 1
            q = 'win'
            sorting_list.append(q)
            symbol_list.append(df['Symbol'][i])
            balance = balance + profit - commission
            print(balance)
            print(profit)
            print(commission)

            trade_history.append(balance)

    num += 1


Total_position = win + lose + both
w = round(win / (win + lose), 2) * 100
e = round(w / 100 * R - (1 - w / 100) * 1, 2)
Total_Gain = Total_position * e

print('Pos =', Total_position)
print('Both =', both)
print('Win =', win)
print('Lose =', lose)
print('w =', w, '%')
print('e =', e)
print('Gain =', Total_Gain)
print(balance)




print(sorting_list)
print(symbol_list)


lose_plot, win_plot, both_plot = [], [], []

df = df[['Symbol', 'Date', 'Open', 'Volume', 'signal', 'result']]

for i in range(0, len(sorting_list)):
    if sorting_list[i] == 'lose':
        lose_plot.append(fig_plot[i])
    if sorting_list[i] == 'win':
        win_plot.append(fig_plot[i])
    if sorting_list[i] == 'both':
        both_plot.append(fig_plot[i])



print(len(lose_plot))
print(len(win_plot))
print(len(both_plot))

'''
for i in range(0, len(win_plot)):
    win_plot[i].write_html('tmp_win' + str(i) + '.html', auto_open=True)
for i in range(0, len(lose_plot)):
    lose_plot[i].write_html('tmp_lose' + str(i) + '.html', auto_open=True)

for i in range(0, len(win_plot)):
    win_plot[i].write_html('tmp_win' + str(i) + '.html', auto_open=False)
for i in range(0, len(lose_plot)):
    lose_plot[i].write_html('tmp_lose' + str(i) + '.html', auto_open=False)
'''
plt.plot(trade_history)
plt.show()  #ezt mindig legutóljára, mert csak bezárása után folytatódik a progi.

'''
df.to_csv(f'C:\\Users\Majer\\PycharmProjects\\pythonProject\\Historical_data\\'
                  f'redwick.csv')

df4 = df.loc[df['Lose'] == 1, ('Symbol', 'Date', 'Volume', 'Open')]

df5 = df.loc[df['Win'] == 1, ('Symbol', 'Date', 'Volume', 'Open')]
df5.to_csv(f'C:\\Users\Majer\\PycharmProjects\\pythonProject\\Historical_data\\'
                  f'redwickwin.csv')


'''
