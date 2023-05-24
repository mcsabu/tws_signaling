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
    scanSub.numberOfRows = 10
    scanSub.abovePrice = 0.75
    scanSub.belowPrice = 20
    scanSub.aboveVolume = 100000
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

        #printed_symbol.append(symbol)
        #printed_symbol.append(defaultid)
        duration = '7200 S'
        resolution = '5 mins'

        #print('Ticker: '+ fileName + ' ')
        #print('Downloading...')
        #print(printed_symbol)
        #Create contract object
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'

        app.reqHistoricalData(defaultid, contract, '', duration, resolution, 'TRADES', 0, 2, False, [])

        time.sleep(0.5)  # sleep to allow enough time for data to be returned


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


def send_email(symbol, date, entry, stoploss, target):
    outlook.username = "ibkralertdumpster@outlook.com"
    outlook.password = "Qwertzui1"

    subject = 'Redwick'
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


def Jump_fail_RTH(df):

    df['OnlyDate'] = pandas.to_datetime(df['Date']).dt.date

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
    param7 = 0.5
    param8 = 200000
    param9 = 1
    param10 = 0.75
    param11 = 3000000
    param12 = 100000

    df['entry'] = 0
    df['stoploss'] = 0
    df['target'] = 0
    df['buy_signal'] = False
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
                                                    df['buy_signal'][l] = True
                                                    df['entry'][l] = entry_price
                                                    df['stoploss'][l] = top_price
                                                    df['target'][l] = start_price
        except KeyError:
            pass


    if df['buy_signal'].iat[-1] == True:
        print('BUYSIGNAL - JUMPFAIL_RTH')
        buy_signal_list.append(df.iloc[-1])
        send_email(df['Symbol'].iloc[-1], df['Date'].iloc[-1],
                   df['entry'].iloc[-1], df['stoploss'].iloc[-1], df['target'].iloc[-1])

        #sound lassítja a folyamatot 2 seccel, lejátszás + continue kéne..
        winsound.PlaySound('C:\\Users\\user\\PycharmProjects\\pythonProject\\'
                           'mixkit-interface-hint-notification-911.wav', winsound.SND_FILENAME)
        #df['buy_signal'].iat[-1] = False # hogy utána ne jelezzen be újra és újra

    else:
        print('NO JUMPFAIL_RTH SIGNAL YET')


def Jump_fail_prem(df):

    df['OnlyDate'] = pandas.to_datetime(df['Date']).dt.date

    strg = "2017-07-20-14-00"
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
    df['entry'] = 0
    df['stoploss'] = 0
    df['target'] = 0
    df['buy_signal'] = False
    param1 = 5
    param2 = 5
    param3 = 5  # 10-nél is jó
    param4 = 1.2  # 1.2-nél is jó
    param5 = 5
    param6 = 10
    param7 = 0.5
    param8 = 100000
    param9 = 1
    param10 = 0.75
    param11 = 1000000
    param12 = 20000
    # param13 = 2.0
    cutoff_index = -1

    for i in df.index:
        if i > cutoff_index:
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
                                                    high_pr1 = df['High'][l - 1];
                                                    high_pr2 = df['High'][l - 2]
                                                    high_pr3 = df['High'][l - 3];
                                                    high_pr4 = df['High'][l - 4]
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
                                                        df['buy_signal'][l] = True
                                                        df['entry'][l] = entry_price
                                                        df['stoploss'][l] = top_price
                                                        df['target'][l] = start_price
            except KeyError:
                pass


    if df['buy_signal'].iat[-1] == True:
        print('BUYSIGNAL - JUMPFAIL_prem')
        buy_signal_list.append(df.iloc[-1])
        send_email(df['Symbol'].iloc[-1], df['Date'].iloc[-1],
                   df['entry'].iloc[-1], df['stoploss'].iloc[-1], df['target'].iloc[-1])

        #sound lassítja a folyamatot 2 seccel, lejátszás + continue kéne..
        winsound.PlaySound('C:\\Users\\Majer\\PycharmProjects\\pythonProject\\trading_bot\\'
                           'mixkit-interface-hint-notification-911.wav', winsound.SND_FILENAME)
        #df['buy_signal'].iat[-1] = False # hogy utána ne jelezzen be újra és újra

    else:
        print('NO JUMPFAIL_prem SIGNAL YET')


def strategy_calculation_for_all_symbol():
    for i in dfs:
        Jump_fail_RTH(i)
        Jump_fail_prem(i)


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

