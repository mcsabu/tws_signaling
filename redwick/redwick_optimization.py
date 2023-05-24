#Optimalization

import winsound
import pandas as pd
import numpy as np
import time
from datetime import datetime


parameter_0 = 'R'
parameter_1 = 'a'
parameter_2 = 'a'
parameter_3 = 'b'
parameter_4 = 'c'
parameter_5 = 'h'
parameter_6 = 'b'
parameter_7 = 'c'
parameter_8 = 'h'
parameter_9 = 'b'
parameter_10 = 'c'



df1 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part1.csv', sep=';')
df2 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part2.csv', sep=';')
df3 = pd.read_csv(
    r'C:\Users\user\PycharmProjects\pythonProject\Micro_List_2Y_5m_part3.csv', sep=';')

df = pd.concat([df1, df2, df3], ignore_index=True)


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
df['-1-3_15m_Volume_mean'] = df[['-1_15m_Volume', '-2_15m_Volume', '-3_15m_Volume']].mean(axis=1)
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

paramteric_study = pd.DataFrame(columns =[parameter_0, parameter_1, parameter_2, parameter_3,
                                                                                  parameter_4,  parameter_5,
                                                                                  parameter_6, parameter_7, parameter_8,
                                                                                  parameter_9, parameter_10,
                                                                                  'Trades', 'Win', 'Lose', 'w', 'e', 'Gain'])
print(paramteric_study)

start = time.time()
count = 0
for ii in np.arange(2, 6, 1): # 4
    R = ii
    for jj in np.arange(0.3, 0.8, 0.2): # 3
        param1 = jj
        for kk in np.arange(0.3, 0.7, 0.3): # 2
            param3 = kk
            for ll in np.arange(1.05, 1.11, 0.05): # 2
                param4 = ll
                for oo in np.arange(0.20, 0.41, 0.20): # 2
                    param5 = oo
                    for pp in np.arange(1, 1001, 999):  # 2
                        param6 = pp
                        for qq in np.arange(0.6, 0.81, 0.2):  # 2
                            param7 = qq
                            for rr in np.arange(0.3, 0.51, 0.2):  # 2
                                param8 = rr
                                for ss in np.arange(1.02, 1.05, 1.01):  # 3
                                    param9 = ss
                                    for tt in np.arange(300000, 800000, 200000):  # 3
                                        param10 = tt
                                        for uu in np.arange(0.7, 1, 0.2):  # 2
                                            param2 = uu


                                            base1 = df['Open'] < 8
                                            base2 = df['Open'] > 1
                                            base3 = df['0_15m_Volume'] > param10  # LIQUIDITY
                                            base4 = 1
                                            base5 = df['OnlyDate'] == df['OnlyDate'].shift(5)
                                            base6 = df['Close'] / df['min_Low'] > param9  # VOLATILITY
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
                                            strat2 = df['min_low_close_diff'] / df['bar_size'] > param1
                                            strat3 = df['max_high_open_diff'] / df['bar_size'] < param8
                                            strat4 = 1
                                            strat5 = df['bar_size'] < param7 * df['bar_size'].shift(3)
                                            strat6 = df['0_15m_Volume'] < param2 * df['0_15m_Volume'].shift(3)  # ezt paraméterezni
                                            strat7 = df['0_15m_Volume'] > param3 * df['0_15m_Volume'].shift(3)  # ezt paraméterezni
                                            strat8 = df['min_Low'] > 1 * df['VWAP']  # minlow
                                            strat9 = 1
                                            strat10 = 1

                                            opt1 = df['VWAP'] > param4 * df['VWAP'].shift(24)
                                            opt2 = 1
                                            opt3 = (df['max_prev45m_High'] - df['VWAP']) * param5 < df['Close'] - df['VWAP']
                                            opt4 = df['Volmax'] != df['Lowmin']
                                            opt5 = 1
                                            opt6 = df['max_Volume'] < param6 * df['min_Volume'].shift(3)
                                            opt7 = 1
                                            opt8 = 1
                                            opt9 = 1
                                            opt10 = 1

                                            # BUY condition
                                            df['signal'] = np.where(base1 & base2 & base3 & base4 & base5 & base6 & base7 & base8 & base10 &
                                                                    strat1 & strat2 & strat3 & strat4 & strat5 & strat6 & strat7 & strat8 & strat9 & strat10 &
                                                                    opt1 & opt2 & opt3 & opt4 & opt5 & opt6 & opt7 & opt8 & opt9 & opt10
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

                                            '''
                                            print('Pos =', Total_position)
                                            print('Win =', win)
                                            print('Lose =', lose)
                                            print('w =', w, '%')
                                            print('e =', e)
                                            print('Gain =', Total_Gain)
                                            '''

                                            result_list = [[R, param1, param2, param3, param4, param5, param6, param7, param8,
                                                        param9, param10, Total_position, win, lose, w, e, Total_Gain]]
                                            print(result_list)
                                            #paramteric_study.append(result_list)

                                            paramteric_study = paramteric_study.append(pd.DataFrame(result_list,
                                                                        columns =[parameter_0, parameter_1, parameter_2, parameter_3,
                                                                                  parameter_4,  parameter_5,
                                                                                  parameter_6, parameter_7, parameter_8,
                                                                                  parameter_9, parameter_10,
                                                                                  'Trades', 'Win', 'Lose', 'w', 'e', 'Gain']),
                                                           ignore_index=True)


                                            count += 1
                                            elapsed_time_fl = (time.time() - start)
                                            print(elapsed_time_fl)



paramteric_study.to_csv(f'C:\\Users\\user\\PycharmProjects\\pythonProject\\redwick\\'
                      f'redwick_parametric_study.csv')

#SORTING  parametric study, according to exp or Gain

elapsed_time_fl = (time.time() - start)
print(count)
print(elapsed_time_fl)





