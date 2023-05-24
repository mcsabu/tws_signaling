#Optimalization

import winsound
import pandas as pd
import numpy as np
import time
from threading import Thread
parameter_1 = 'R'
parameter_2 = 'max_high_to_VWAP'
parameter_3 = ''

df4 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part10.csv', sep=';')
df5 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part11.csv', sep=';')

df6 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part12.csv', sep=';')
df7 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part13.csv', sep=';')


df8 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part14.csv', sep=';')

df9 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part15.csv', sep=';')

df = pd.concat([df4, df5, df6, df7, df8, df9], ignore_index=True)



df['-2_Open'] = df['Open'].shift(2)
df['-1_High'] = df['High'].shift(1);
df['-2_High'] = df['High'].shift(2)
df['-1_Low'] = df['Low'].shift(1);
df['-2_Low'] = df['Low'].shift(2);
df['-3_Low'] = df['Low'].shift(3)
df['-4_Low'] = df['Low'].shift(4);
df['-5_Low'] = df['Low'].shift(5);
df['-6_Low'] = df['Low'].shift(6)
df['-7_Low'] = df['Low'].shift(7);
df['-8_Low'] = df['Low'].shift(8);
df['-9_Low'] = df['Low'].shift(9)
df['-10_Low'] = df['Low'].shift(10);
df['-11_Low'] = df['Low'].shift(11);
df['-12_Low'] = df['Low'].shift(12)
df['-13_Low'] = df['Low'].shift(13);
df['-14_Low'] = df['Low'].shift(14);
df['-15_Low'] = df['Low'].shift(15)
df['-16_Low'] = df['Low'].shift(16);
df['-17_Low'] = df['Low'].shift(17);
df['-18_Low'] = df['Low'].shift(18)

df['Volume_1'] = df['Volume'].shift(1);
df['Volume_2'] = df['Volume'].shift(2)

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
df['-1-3_15m_Volume_mean'] = df[['-1_15m_Volume', '-2_15m_Volume', '-3_15m_Volume']].mean(axis=1)

df['min_prev45m_Low'] = df[['-3_Low', '-4_Low', '-5_Low', '-6_Low', '-7_Low', '-8_Low', '-9_Low',
                            '-10_Low', '-11_Low', '-12_Low']].min(axis=1)

df['min_prev75m_Low'] = df[['-3_Low', '-4_Low', '-5_Low', '-6_Low', '-7_Low', '-8_Low', '-9_Low',
                            '-10_Low', '-11_Low', '-12_Low', '-13_Low', '-14_Low',
                            '-15_Low', '-16_Low', '-17_Low', '-18_Low']].min(axis=1)
df['OnlyDate'] = pd.to_datetime(df['Date']).dt.date


def VWAP(df):
    H = df.High
    L = df.Low
    C = df.Close
    V = df.Volume
    return df.assign(VWAP=(V * ((H+L+C)/3)).cumsum() / V.cumsum())
df = df.groupby(['OnlyDate', 'Symbol'], group_keys=False).apply(VWAP)

paramteric_study = pd.DataFrame(columns =[parameter_1, 'Trades', 'Win', 'Lose', 'w', 'e', 'Gain'])


paramteric_study2 = pd.DataFrame(columns =[parameter_1, 'Trades', 'Win', 'Lose', 'w', 'e', 'Gain'])


start = time.time()
count = 0

for ii in np.arange(1, 7, 0.5): # 14db
    R = ii


    a = df['min_low_close_diff'] / df['bar_size'] > 0.5
    b = df['max_high_open_diff'] / df['bar_size'] < 0.2
    c = df['0_15m_Volume'] > 300000
    d = df['0_15m_Volume'] < 5000000
    e = df['0_15m_Volume'] < 0.8 * df['0_15m_Volume'].shift(3)
    f = df['0_15m_Volume'] < 0.8 * df['0_15m_Volume'].shift(6)
    g = df['0_15m_Volume'] < 0.8 * df['0_15m_Volume'].shift(9)
    h = df['bar_size'] < 1 * df['bar_size'].shift(3)
    i = df['bar_size'] < 1 * df['bar_size'].shift(9)
    j = df['Close'] < 1 * df['Close'].shift(3)
    k = df['-3_15m_Volume'] > 300000
    l = df['Volmax'] != df['Lowmin']  # érdekes, pont fordítva, mint gondoltam...megnézni, több adatra.
    m = df['max_High'] < df['max_High'].shift(3)
    n = df['max_High'] < df['max_High'].shift(6)
    o = df['OnlyDate'] == df['OnlyDate'].shift(-9)
    p = df['Close'] - df['-2_Open'] < 0
    q = df['OnlyDate'] == df['OnlyDate'].shift(3)
    r = df['Open'] < 3
    s = df['Open'] > 0.75  # ezzel kevesebb a retunr, de talán jobban szűrt; 0,75 és 3 között 1+e, mindegyiknél?
    t = df['Close'] > 1 * df['VWAP']
    u = 1

    # BUY condition
    df['signal'] = np.where(a & b & c & d & e & f & g & h & i & j & k & l & m & n & o & p & q & r & s & t & u
                            , 1, np.nan)

    # TARGET
    df['R'] = R * (df['Close'] - df['min_Low'])
    df['target_R'] = df['Close'] + df['R']

    df['result'] = 0

    pos = 0
    lose = 0
    win = 0
    num = 0

    for i in df.index:

        if (df['signal'][i] == 1):
            # ENTRY
            if (pos == 0):
                bp = df["Close"][i]
                pos = 1
                stl = df['min_Low'][i]
                target = df['target_R'][i]
                print("ENTRY = " + str(bp))
                # print(str(stl))
                # print(str(target))

        elif (pos == 1):
            # STOPLOSS
            if (df['Low'][i] < stl):
                pos = 0
                sp = stl
                print("STOP = " + str(sp))
                df[df['result'][i]] = -1
                lose += 1

                # sp és bp gain és stb statisztika követése
            # EXIT
            elif (df['High'][i] > target):
                pos = 0
                sp = target
                print("SELL = " + str(sp))
                df[df['result'][i]] = 1
                win += 1

        num += 1

    Total_position = win + lose
    w = round(win / (win + lose), 2) * 100
    e = round(w / 100 * R - (1 - w / 100) * 1, 2)
    Total_Gain = Total_position * e

    print('')
    print('Pos =', Total_position)
    print('Win =', win)
    print('Lose =', lose)
    print('w =', w, '%')
    print('e =', e)
    print('Gain =', Total_Gain)


    result_list = [[R, Total_position, win, lose, w, e, Total_Gain]]
    print(result_list)
    #paramteric_study.append(result_list)
    paramteric_study2 = paramteric_study2.append(pd.DataFrame(result_list,
                                columns =[parameter_1, 'Trades', 'Win', 'Lose', 'w', 'e', 'Gain']),
                   ignore_index=True)


    count += 1
    elapsed_time_fl = (time.time() - start)
    print(elapsed_time_fl)



paramteric_study.to_csv(f'C:\\Users\user\\PycharmProjects\\pythonProject\\'
                      f'parametric_study.csv')

#SORTING  parametric study, according to exp or Gain

elapsed_time_fl = (time.time() - start)
print(count)
print(elapsed_time_fl)
winsound.PlaySound('C:\\Users\\Majer\\PycharmProjects\\pythonProject\\trading_bot\\'
                           'mixkit-interface-hint-notification-911.wav', winsound.SND_FILENAME)




