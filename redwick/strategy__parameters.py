'''Bull redwick 1.0:
4-9 df (33% data) alapján 54pos/R=3/35%/e=0,4
11-18 (-17) (2. 33% data) alapján 32pos/R=3/34%/e=0,36
Úgy tűnik, hogy univerzálisan működik.
CSAK a LOSEREKET MEGNÉZNI és AZ ALAPJÁN KIZÁRNI PÁR DARABOT.

Még pár egyértelmű lose-t ki kellene szedni, atán mehetne egy paraméteres vizsgálat, kb. 30-40 pos és 0.5-0.6 exp kéne.
'''

R = 3

base1 = df['Open'] < 8
base2 = df['Open'] > 1
base3 = df['0_15m_Volume'] > 300000 #LIQUIDITY EZT mindenképpen paraméteresen megnézni!! 500k-nál 0,5-ös exp. Megéri?
base4 = 1
base5 = df['OnlyDate'] == df['OnlyDate'].shift(5)
base6 = df['Close'] / df['min_Low'] > 1.03 #VOLATILITY ez talán lehetne 1.02
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
strat6 = df['0_15m_Volume'] < 0.8 * df['0_15m_Volume'].shift(3)
strat7 = 1 #df['0_15m_Volume'] > 0.4 * df['0_15m_Volume'].shift(3) #ezt paraméterezni
strat8 = df['min_Low'] > 1 * df['VWAP'] #minlow
strat9 = 1
strat10 = 1


opt1 = df['VWAP'] > 1.05 * df['VWAP'].shift(24)
opt2 = 1
opt3 = (df['max_prev45m_High'] - df['VWAP']) * 0.33 < df['Close'] - df['VWAP']
opt4 = 1
opt5 = 1
opt6 = 1
opt7 = 1
opt8 = 1
opt9 = 1
opt10 = 1