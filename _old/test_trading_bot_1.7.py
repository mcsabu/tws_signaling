from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.scanner import ScannerSubscription
from ib_insync import *
import threading
import time
from datetime import datetime, timedelta
import winsound
import pandas
from pandas import *
import numpy as np
from redmail import outlook



reqID_list = []


buy_signal_list = []
dfs = list()
update_timing_list = []
defaultid = 0

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []  # Initialize variable to store candle

    def historicalData(self, reqId, bar):
        #print("{},{},{},{},{},{}"
        #.format(bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume))
        self.data.append([reqId, bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])

    def scannerData(self, reqId, rank, contracDeatils, distance, benchmark, projection, legsStr):
        super().scannerData(reqId, rank, contracDeatils, distance, benchmark, projection, legsStr)
        print("ScannerData. ReqId:", reqId, contracDeatils.contract.symbol, rank)
        self.data.append([reqId, contracDeatils.contract.symbol])


def top_pc_gain_Scan(asset_type="STK", asset_loc="STK.US.MAJOR", scan_code="TOP_PERC_GAIN"):
    scanSub = ScannerSubscription()
    scanSub.numberOfRows = 50
    scanSub.abovePrice = 0.90
    scanSub.belowPrice = 20
    scanSub.aboveVolume = 200000
    scanSub.MarketCapBelow = 800000000
    scanSub.instrument = asset_type
    scanSub.locationCode = asset_loc
    scanSub.scanCode = scan_code
    return scanSub

def most_active_Scan(asset_type="STK", asset_loc="STK.US.MAJOR", scan_code="MOST_ACTIVE"):
    scanSub = ScannerSubscription()
    scanSub.numberOfRows = 50
    scanSub.abovePrice = 0.90
    scanSub.belowPrice = 30
    scanSub.MarketCapBelow = 800000000
    scanSub.aboveVolume = 200000
    scanSub.instrument = asset_type
    scanSub.locationCode = asset_loc
    scanSub.scanCode = scan_code
    return scanSub

def run_loop():
    app.run()


app = IBapi()
app.connect('127.0.0.1', 7496, 120)


api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)

def getScanner():
    app.reqScannerSubscription(1, top_pc_gain_Scan(), [], [])
    time.sleep(3)
    df_scan_local = pandas.DataFrame(app.data, columns=['reqID', 'Symbol'])
    for i in range(1, len(df_scan_local['Symbol']) + 1):
        reqID_list.append(i)
    df_scan_local.reqID = reqID_list
    reqID_list.clear()
    print(df_scan_local)
    df_scan_local.to_csv(r'C:\Users\user\PycharmProjects\pythonProject\scanner_list.csv', index=False)
    app.cancelScannerSubscription(1)
    app.data.clear()


def getData(contracts, defaultid, scan):
    for i in contracts:
        symbol = i
        fileName = i

        defaultid += 1

        duration = '10800 S'
        resolution = '5 mins'

        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'

        app.reqHistoricalData(defaultid, contract, '', duration, resolution, 'TRADES', 0, 2, False, [])

        time.sleep(0.75)  # sleep to allow enough time for data to be returned


        df = pandas.DataFrame(app.data, columns=['reqID', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        df['Date'] = pandas.to_datetime(df['Date'], unit='s')

        df.Volume *= 100



        df = pandas.merge(scan, df, on='reqID')
        print(df.head(1), df.tail(1))
        df.to_csv(f'C:\\Users\\user\\PycharmProjects\\pythonProject\\'
               f'trading_list_datas.csv', index=False)
    app.data.clear()



def prepare_data_into_individual_frames(df0):
    dfs.clear()
    df0['Date'] = pandas.to_datetime(df0['Date'])

    Symbol_frame = df0['Symbol'].drop_duplicates(keep='first')
    Symbol_list = Symbol_frame.tolist()

    for i in range(len(Symbol_list)):
        locals()['df_' + str(i)] = (df0[df0.Symbol == Symbol_list[i]])
        dfs.append(locals()['df_' + str(i)])

    return dfs


def send_email(strategy, symbol, date, entry, stoploss, target):
    outlook.username = "ibkralertdumpster@outlook.com"
    outlook.password = "Qwertzui1"

    subject = str(strategy)
    text = str(symbol) + '\n' \
           + str(date) + '\n' \
           + 'Entry: ' + str(entry) + '\n' \
           + 'Stoploss: ' + str(stoploss) + '\n' \
           + 'Target: ' + str(target) + '\n' \

    outlook.send(
        receivers=["ibkralertdumpster@outlook.com"],
        subject=subject,
        text=text
    )

def Green_climb_prem_short(df):
    df['barsize'] = df.High - df.Low
    df['OnlyDate'] = pandas.to_datetime(df['Date']).dt.date
    df['entry'] = 0; df['stoploss'] = 0; df['target'] = 0
    strategy = ''
    alert = False
    strg = "2017-07-20-14-00"
    dt = datetime.strptime(strg, '%Y-%m-%d-%H-%M')
    tme = dt.time()
    df['OnlyTime'] = pandas.to_datetime(df['Date']).dt.time
    df['mid'] = (df.High + df.Low) / 2

    for i in df.index:
        signal = 0
        try:
            if (df.Volume[i] > 50000) & (df.Close[i] > 1):
                if (df.Close[i] > df.Open[i]) & (signal == 0) \
                        & (df['OnlyTime'][i] < tme) \
                        & (df.OnlyDate[i] == df.OnlyDate[i - 5]):
                    for b in range(i - 10, i + 1):
                        if (df.OnlyDate[b] == df.OnlyDate[i]) & (df.Close[b] / df.Low[b] > 1.10):
                            for c in range(b, i + 0):
                                if (df.mid[c] < df.High[b]) & (df.OnlyDate[c] == df.OnlyDate[i]) \
                                        & (df.mid[c] > df.mid[b]):
                                    if (i - b > 2) & (i - b < 8):
                                        prev_low = df.Low[b + 1]
                                        for k in range(b + 1, i + 0):
                                            if df.Low[k] > prev_low:
                                                pass
                                            if df.Low[k] < prev_low:
                                                prev_low = df.Low[k]
                                            if (k == i - 1):
                                                if (df.Close[i] > df.High[b]) & (df.Volume[b] > 200000):
                                                    entry_price = df.Close[i]
                                                    entry_date = df.Date[i]
                                                    if entry_price / prev_low > 1.02:
                                                        if df.index[-1] == i:
                                                            alert = True
                                                            R = entry_price - prev_low
                                                            df['entry'][i] = entry_price
                                                            df['stoploss'][i] = entry_price + 2 * R
                                                            df['target'][i] = entry_price - 1 * R
                                                            strategy = 'Green_climb_prem_short'
        except KeyError:
            pass

    if alert == True:
        print('SELLSIGNAL - Green_climb_prem_short')
        buy_signal_list.append(df.iloc[-1])
        send_email(strategy, df['Symbol'].iloc[-1], df['Date'].iloc[-1],
                   df['entry'].iloc[-1], df['stoploss'].iloc[-1], df['target'].iloc[-1])

        winsound.PlaySound('C:\\Users\\user\\PycharmProjects\\pythonProject\\'
                           'mixkit-interface-hint-notification-911.wav', winsound.SND_FILENAME)

    else:
        print('NO GREEN_CLIMB_PREM_SHORT SIGNAL YET')


def Cons_breakout(df):

    df['barsize'] = df.High - df.Low
    df['OnlyDate'] = pandas.to_datetime(df['Date']).dt.date
    df['entry'] = 0; df['stoploss'] = 0; df['target'] = 0
    strategy = ''
    alert = False
    def VWAP(df):
        H = df.High
        L = df.Low
        C = df.Close
        V = df.Volume
        return df.assign(VWAP=(V * ((H + L + C) / 3)).cumsum() / V.cumsum())

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
    df['OnlyTime'] = pandas.to_datetime(df['Date']).dt.time

    for i in df.index:
        signal = 0
        try:
            if (df['Bollinger_diff'][i] * param5 < df['Bollinger_max'][i - 3]):
                if (df.avg_volume[i - 1] > param1) & (df.Volume[i] > param2) & (df.Close[i] > param3):
                    if (df.Close[i] > df.Open[i]) & (signal == 0) \
                            & (df['OnlyTime'][i] < tme) \
                            & (df.OnlyDate[i] == df.OnlyDate[i - 25]) \
                            & (df.High[i] > df.VWAP[i]) \
                            & (df.High[i] > df.prev_max[i - 1]):
                        entry_price = df.prev_max[i - 1]
                        entry_date = df.Date[i]
                        prev_low = df.prev_min[i]
                        if entry_price / prev_low > 1.02:
                            if df.index[-1] == i:
                                alert = True
                                df['entry'][i] = entry_price
                                df['stoploss'][i] = prev_low
                                df['target'][i] = entry_price + 2*(entry_price-prev_low)
                                strategy = 'Cons_breakout'

        except KeyError:
            pass

    if alert == True:
        print('BUYSIGNAL - CONS_BREAKOUT')
        buy_signal_list.append(df.iloc[-1])
        send_email(strategy, df['Symbol'].iloc[-1], df['Date'].iloc[-1],
                   df['entry'].iloc[-1], df['stoploss'].iloc[-1], df['target'].iloc[-1])

        #sound lassítja a folyamatot 2 seccel, lejátszás + continue kéne..
        winsound.PlaySound('C:\\Users\\user\\PycharmProjects\\pythonProject\\'
                           'mixkit-interface-hint-notification-911.wav', winsound.SND_FILENAME)


    else:
        print('NO CONS_BREAKOUT SIGNAL YET')

def Green_bounce_inclusive(df):
    df['OnlyDate'] = pandas.to_datetime(df['Date']).dt.date
    max_list = []
    strg = "2017-07-20-19-30"
    dt = datetime.strptime(strg, '%Y-%m-%d-%H-%M')
    tme = dt.time()
    df['OnlyTime'] = pandas.to_datetime(df['Date']).dt.time
    df['entry'] = 0; df['stoploss'] = 0; df['target'] = 0
    alert = False
    strategy = ''
    for i in df.index:
        signal = 0
        try:
            if (df.Volume[i] > 250000) & (df.Close[i] > 1):
                if df.High[i] != df.Low[i]:
                    if (df.Close[i] > df.Open[i]) \
                            & ((df.High[i] - df.Close[i]) / (df.High[i] - df.Low[i]) < 0.75) \
                            & (df.Close[i] > df.Close[i - 1]) \
                            & (df.High[i] / df.Low[i] > 1.10):
                        start_price = df.Low[i]
                        start_date = df.Date[i]
                        top_price = df.High[i]
                        top_date = df.Date[i]
                        breaking = 0
                        for j in range(i, i + 30):
                            if (signal == 0):
                                if (df.High[j] > top_price) & (
                                        df.Low[j] > start_price + (top_price - start_price) * 1 / 3) \
                                        & (breaking == 0):
                                    top_price = df.High[j]
                                    top_date = df.Date[j]
                                elif (df.High[j] < top_price) & (
                                        df.Low[j] > start_price + (top_price - start_price) * 1 / 3) \
                                        & (breaking == 0):
                                    pass
                                elif (df.High[j] < top_price) & (
                                        df.Low[j] < start_price + (top_price - start_price) * 1 / 3):
                                    entry_price = (df.Low[j] + df.Close[j]) / 2
                                    entry_date = df.Date[j]
                                    breaking = 1
                                    if (df.OnlyTime[j] < tme) & (df.OnlyDate[j] == df.OnlyDate[i - 1]) \
                                            & (j - i < 10):
                                        if df.index[-1] == j:
                                            alert = True
                                            df['entry'][j] = entry_price
                                            df['stoploss'][j] = start_price
                                            df['target'][j] = (start_price + top_price) / 2
                                            strategy = 'Green_bounce_inclusive'
        except KeyError:
            pass

    if alert == True:
        print('BUYSIGNAL - GREEN_BOUNCE_INCLUSIVE')
        buy_signal_list.append(df.iloc[-1])
        send_email(strategy, df['Symbol'].iloc[-1], df['Date'].iloc[-1],
                   df['entry'].iloc[-1], df['stoploss'].iloc[-1], df['target'].iloc[-1])

        winsound.PlaySound('C:\\Users\\user\\PycharmProjects\\pythonProject\\'
                           'mixkit-interface-hint-notification-911.wav', winsound.SND_FILENAME)

    else:
        print('NO GREEN_BOUNCE_INCLUSIVE SIGNAL YET')

def Green_bounce(df):
    df['OnlyDate'] = pandas.to_datetime(df['Date']).dt.date
    max_list = []
    strg = "2017-07-20-18-30"
    dt = datetime.strptime(strg, '%Y-%m-%d-%H-%M')
    tme = dt.time()
    df['OnlyTime'] = pandas.to_datetime(df['Date']).dt.time
    df['entry'] = 0; df['stoploss'] = 0; df['target'] = 0
    alert = False
    strategy = ''
    for i in df.index:

        signal = 0
        try:
            if (df.Volume[i] > 300000) & (df.Close[i] > 1):
                if df.High[i] != df.Low[i]:
                    if (df.Close[i] > df.Open[i]) \
                            & ((df.High[i] - df.Close[i]) / (df.High[i] - df.Low[i]) < 0.5) \
                            & (df.Close[i] > df.Close[i - 1]) \
                            & (df.High[i] / df.Low[i] > 1.15):
                        start_price = df.Low[i]
                        start_date = df.Date[i]
                        top_price = df.High[i]
                        top_date = df.Date[i]
                        for j in range(i, i + 30):
                            if (signal == 0):
                                if (df.High[j] > top_price):
                                    top_price = df.High[j]
                                    top_date = df.Date[j]
                                else:
                                    for k in range(j + 1, j + 30):
                                        if (signal == 0) & (df.High[k] < top_price):
                                            if (df.Low[k] < (start_price + (top_price - start_price) * 1 / 4)) \
                                                    & (k - j < 7) \
                                                    & (j - i < 5):  # ezeket átgondolni, leht távolabbi is oké
                                                for l in range(j + 1, k):
                                                    if (signal == 0):
                                                        max_list.append(df.High[l])
                                                        if top_price >= max(max_list):

                                                            entry_price = (df.Low[k] + df.Close[k]) / 2
                                                            entry_date = df.Date[k]
                                                            max_list.clear()
                                                            if (df.OnlyTime[k] < tme) & (
                                                                    df.OnlyDate[k] == df.OnlyDate[i - 1]):
                                                                if df.index[-1] == k:
                                                                    alert = True
                                                                    df['entry'][k] = entry_price
                                                                    df['stoploss'][k] = start_price
                                                                    df['target'][k] = (start_price + top_price)/2
                                                                    strategy = 'Green_bounce'

        except KeyError:
            pass

    if alert == True:
        print('BUYSIGNAL - GREEN_BOUNCE')
        buy_signal_list.append(df.iloc[-1])
        send_email(strategy, df['Symbol'].iloc[-1], df['Date'].iloc[-1],
                   df['entry'].iloc[-1], df['stoploss'].iloc[-1], df['target'].iloc[-1])

        winsound.PlaySound('C:\\Users\\user\\PycharmProjects\\pythonProject\\'
                           'mixkit-interface-hint-notification-911.wav', winsound.SND_FILENAME)

    else:
        print('NO GREEN_BOUNCE SIGNAL YET')

def Jump_fail_RTH(df):

    df['OnlyDate'] = pandas.to_datetime(df['Date']).dt.date
    strategy = ''
    def VWAP(df):
        H = df.High
        L = df.Low
        C = df.Close
        V = df.Volume
        return df.assign(VWAP=(V * ((H + L + C) / 3)).cumsum() / V.cumsum())

    df = df.groupby(['OnlyDate', 'Symbol'], group_keys=False).apply(VWAP)

    param1 = 5
    param2 = 5
    param3 = 5
    param4 = 1.2
    param5 = 5
    param6 = 10
    param7 = 0.4
    param8 = 200000
    param9 = 1
    param10 = 0.75
    param11 = 3000000
    param12 = 100000
    alert = False
    df['entry'] = 0; df['stoploss'] = 0; df['target'] = 0

    for i in df.index:
        signal = 0
        try:
            if (df['Volume'][i] > param1 * df['Volume'][i - 1]):
                if ((df['High'][i] - df['Low'][i]) > param2 * (df['High'][i - 1] - df['Low'][i - 1])):
                    if (signal == 0):
                        start_price = df['Close'][i - 1]
                        start_price_1 = df['High'][i - 2];
                        start_price_2 = df['High'][i - 5]
                        start_price_3 = df['High'][i - 10]
                        start_price_max = max(start_price_1, start_price_2, start_price_3)
                        start_jump_volume = df['Volume'][i]
                        start_volume = df['Volume'][i - 1]
                        start_date = df['Date'][i - 1]
                        #start_only_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
                        start_only_date = start_date.date()
                        for j in range(i, i + param3):
                            if (df['High'][j] > start_price * param4) & (signal == 0):  # EZT ÁT KELL ÍRNI
                                for k in range(j, j + param5):
                                    if (signal == 0) & (df['High'][k] < df['High'][k - 1]):
                                        top_price = df['High'][k - 1]
                                        top_date = df['Date'][k - 1]
                                        #top_only_date = datetime.strptime(top_date, '%Y-%m-%d %H:%M:%S')
                                        top_only_date = top_date.date()
                                        top_volume = df['Volume'][k - 1]
                                        top_volume_next1 = df['Volume'][k]
                                        top_vwap = df['VWAP'][k - 1]
                                        for l in range(k, k + param6):
                                            if ((top_price + start_price) / 2 > start_price_max):
                                                entry_signal = df['Low'][l]
                                                entry_price = df['Close'][l]
                                                high_pr1 = df['High'][l - 1];
                                                high_pr2 = df['High'][l - 2]
                                                high_pr3 = df['High'][l - 3];
                                                high_pr4 = df['High'][l - 4]
                                                max_prev = max(high_pr1, high_pr2, high_pr3, high_pr4)
                                                entry_date = df['Date'][l]
                                                entry_only_date = df['OnlyDate'][l]
                                                if (((top_price - entry_signal) / (top_price - start_price)) > param7) \
                                                        & ((top_price - entry_signal) / (
                                                        top_price - start_price) < param10) \
                                                        & (entry_price > param9) & (top_volume > param8) \
                                                        & (start_only_date == top_only_date) \
                                                        & (start_only_date == entry_only_date) \
                                                        & (entry_price < top_price) \
                                                        & (top_price >= max_prev) \
                                                        & (top_volume < param11) \
                                                        & (top_volume_next1 > param12):
                                                    if df.index[-1] == l:
                                                        alert = True
                                                        df['entry'][l] = entry_price
                                                        df['stoploss'][l] = 2 / 3 * (top_price - entry_price) + entry_price
                                                        df['target'][l] = start_price
                                                        strategy = 'Jumpfail_RTH'
        except KeyError:
            pass

    if alert == True:
        print('BUYSIGNAL - JUMPFAIL_RTH')
        buy_signal_list.append(df.iloc[-1])
        send_email(strategy, df['Symbol'].iloc[-1], df['Date'].iloc[-1],
                   df['entry'].iloc[-1], df['stoploss'].iloc[-1], df['target'].iloc[-1])

        winsound.PlaySound('C:\\Users\\user\\PycharmProjects\\pythonProject\\'
                           'mixkit-interface-hint-notification-911.wav', winsound.SND_FILENAME)

    else:
        print('NO JUMPFAIL_RTH SIGNAL YET')

def Jump_fail_prem(df):

    df['OnlyDate'] = pandas.to_datetime(df['Date']).dt.date
    strategy =''
    strg = "2017-07-20-19-00" #ezt kiszedtem
    dt = datetime.strptime(strg, '%Y-%m-%d-%H-%M')
    tme = dt.time()
    df['OnlyTime'] = pandas.to_datetime(df['Date']).dt.time

    def VWAP(df):
        H = df.High
        L = df.Low
        C = df.Close
        V = df.Volume
        return df.assign(VWAP=(V * ((H + L + C) / 3)).cumsum() / V.cumsum())

    df = df.groupby(['OnlyDate', 'Symbol'], group_keys=False).apply(VWAP)
    df['entry'] = 0; df['stoploss'] = 0; df['target'] = 0

    param1 = 5
    param2 = 5
    param3 = 5  # 10-nél is jó
    param4 = 1.15  # 1.2-nél is jó
    param5 = 5
    param6 = 10
    param7 = 0.40
    param8 = 100000
    param9 = 1
    param10 = 0.90
    param11 = 10000000
    param12 = 10000
    alert = False
    for i in df.index:
            signal = 0
            try:
                if (df['Volume'][i] > param1 * df['Volume'][i - 1]) & (df['OnlyTime'][i] < tme):
                    if ((df['High'][i] - df['Low'][i]) > param2 * (df['High'][i - 1] - df['Low'][i - 1])):
                        if (signal == 0):
                            start_price = df['Close'][i - 1]
                            start_price_1 = df['High'][i - 2];
                            start_price_2 = df['High'][i - 5]
                            start_price_3 = df['High'][i - 10]
                            start_price_max = max(start_price_1, start_price_2, start_price_3)
                            start_jump_volume = df['Volume'][i]
                            start_volume = df['Volume'][i - 1]
                            start_date = df['Date'][i - 1]
                            #start_only_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
                            start_only_date = start_date.date()
                            for j in range(i, i + param3):
                                if (df['High'][j] > start_price * param4) & (signal == 0):  # EZT ÁT KELL ÍRNI
                                    for k in range(j, j + param5):

                                        if (signal == 0) & (df['High'][k] < df['High'][k - 1]):
                                            top_price = df['High'][k - 1]
                                            top_date = df['Date'][k - 1]
                                            #top_only_date = datetime.strptime(top_date, '%Y-%m-%d %H:%M:%S')
                                            top_only_date = top_date.date()
                                            top_volume = df['Volume'][k - 1]
                                            top_volume_next1 = df['Volume'][k]
                                            top_vwap = df['VWAP'][k - 1]
                                            for l in range(k, k + param6):
                                                if ((top_price + start_price) / 2 > start_price_max):
                                                    entry_signal = df['Low'][l]
                                                    entry_price = df['Close'][l]
                                                    high_pr1 = df['High'][l - 1]; high_pr2 = df['High'][l - 2]
                                                    high_pr3 = df['High'][l - 3]; high_pr4 = df['High'][l - 4]
                                                    max_prev = max(high_pr1, high_pr2, high_pr3, high_pr4)
                                                    entry_date = df['Date'][l]
                                                    entry_only_date = df['OnlyDate'][l]
                                                    if (((top_price - entry_signal) / (
                                                            top_price - start_price)) > param7) \
                                                            & ((top_price - entry_signal) / (
                                                            top_price - start_price) < param10) \
                                                            & (entry_price > param9) & (top_volume > param8) \
                                                            & (entry_only_date == top_only_date) \
                                                            & (entry_price < top_price) \
                                                            & (top_price >= max_prev) \
                                                            & (top_volume < param11) \
                                                            & (top_volume_next1 > param12) \
                                                            & (l - (k - 1) < 5):
                                                        if df.index[-1] == l:
                                                            alert = True
                                                            df['entry'][l] = entry_price
                                                            df['stoploss'][l] = 2 / 3 * (top_price - entry_price) + entry_price
                                                            df['target'][l] = start_price
                                                            strategy = 'Jumpfail_prem'
            except KeyError:
                pass

    if alert == True:
        print('BUYSIGNAL - JUMPFAIL_prem')
        buy_signal_list.append(df.iloc[-1])
        send_email(strategy, df['Symbol'].iloc[-1], df['Date'].iloc[-1],
                   df['entry'].iloc[-1], df['stoploss'].iloc[-1], df['target'].iloc[-1])

        winsound.PlaySound('C:\\Users\\Majer\\PycharmProjects\\pythonProject\\trading_bot\\'
                           'mixkit-interface-hint-notification-911.wav', winsound.SND_FILENAME)

    else:
        print('NO JUMPFAIL_prem SIGNAL YET')


def strategy_calculation_for_all_symbol():
    for i in dfs:
        Jump_fail_RTH(i)
        Jump_fail_prem(i)
        Green_bounce(i)
        Green_bounce_inclusive(i)
        Cons_breakout(i)
        #Green_climb_prem_short(i)


def running():
    increment = 0
    for i in range(0, 144): #Teljes market day
        current_time = datetime.now().strftime('%H:%M:%S')
        update_time = (datetime(year = 2023, month = 10, day = 12, hour = 10, minute = 00, second = 5) +
               timedelta(minutes=increment)).strftime('%H:%M:%S')
        increment = increment + 5
        if update_time > current_time:
            update_timing_list.append(update_time)
            print(update_time)

    i = 0
    for i in range(len(update_timing_list)):
        current_time = datetime.now().strftime('%H:%M:%S')
        while current_time < update_timing_list[i]:
            current_time = datetime.now().strftime('%H:%M:%S')
            print(datetime.now().strftime('%H:%M:%S'))
            time.sleep(5)
            print(i)
        else:
            getScanner()
            scan = pandas.read_csv(
                r'C:\Users\user\PycharmProjects\pythonProject\scanner_list.csv')
            contracts = scan['Symbol'].tolist()
            getData(contracts, defaultid, scan)
            app.data = []
            print('updating_data')
            print(datetime.now().strftime('%H:%M:%S'))
            df0 = read_csv(r'C:\Users\user\PycharmProjects\pythonProject\trading_list_datas.csv')
            prepare_data_into_individual_frames(df0)
            strategy_calculation_for_all_symbol()
            print(buy_signal_list)

            #Csak az új buy signalról lenne jó ha küldene adatot... Szerencsére így is beazonosítható azért...




running()

#app.disconnect()

