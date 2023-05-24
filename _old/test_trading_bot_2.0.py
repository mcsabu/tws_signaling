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


def run_loop():
    app.run()


app = IBapi()
app.connect('127.0.0.1', 7496, 100)


api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)


def getData(contracts, defaultid, scan):
    for i in contracts:
        symbol = i
        fileName = i

        defaultid += 1

        duration = '5 D'
        resolution = '15 mins'

        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'

        app.reqHistoricalData(defaultid, contract, '', duration, resolution, 'TRADES', 1, 2, False, [])

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


def LC_VWAP_LONG(df):

    df['OnlyDate'] = pandas.to_datetime(df['Date']).dt.date

    def VWAP(df):
        H = df.High
        L = df.Low
        C = df.Close
        V = df.Volume
        return df.assign(VWAP=(V * ((H + L + C) / 3)).cumsum() / V.cumsum())

    df = df.groupby(['OnlyDate', 'Symbol'], group_keys=False).apply(VWAP)
    cutoff_index = -1
    df['entry'] = ''; df['stoploss'] = 0; df['target'] = 0
    alert = False
    strategy = ''
    for i in df.index:
        if i > cutoff_index:
            signal = 0
            breaking = 0
            try:
                if (df.OnlyDate[i] > df.OnlyDate[i - 1]) & (breaking == 0):
                    open_price = df.Open[i]
                    found = 0
                    for j in range(i, i + 150):
                        if (df.OnlyDate[j] < df.OnlyDate[j + 1]) & (breaking == 0) & (found == 0):
                            close_price = df.Close[j]
                            close_vwap = df.VWAP[j]
                            found = 1
                            if (close_price - open_price > 0) & (close_price / open_price > 1.02) \
                                    & (close_price > close_vwap):  # 1.02 és 1.03 is mukodik
                                if ((close_price - close_vwap) / (close_price - open_price) > 0.10) \
                                        & ((close_price - close_vwap) / (close_price - open_price) < 0.30):
                                    for k in range(i + 6, j + 1):
                                        if (df.Low[k] < df.VWAP[k]) & (breaking == 0):
                                            breaking = 1
                                            cutoff_index = k
                                        if (k == j) & (breaking == 0):
                                            if (signal == 0):
                                                if df.index[-1] == j:
                                                    alert = True
                                                    R = close_price - close_vwap
                                                    df['entry'][j] = 'if open > close'
                                                    df['stoploss'][j] = 0.1*R
                                                    df['target'][j] = 2*R
                                                    strategy = 'LC_VWAP_LONG'
            except KeyError:
                pass

    if alert == True:
        print('BUYSIGNAL - LC_VWAP_LONG')
        buy_signal_list.append(df.iloc[-1])
        send_email(strategy, df['Symbol'].iloc[-1], df['Date'].iloc[-1],
                   df['entry'].iloc[-1], df['stoploss'].iloc[-1], df['target'].iloc[-1])

        winsound.PlaySound('C:\\Users\\user\\PycharmProjects\\pythonProject\\'
                           'mixkit-interface-hint-notification-911.wav', winsound.SND_FILENAME)

    else:
        print('NO LC_VWAP_LONG FOUND')


def strategy_calculation_for_all_symbol():
    for i in dfs:
        LC_VWAP_LONG(i)


def running():
    scan = pandas.read_csv(
        r'C:\Users\user\PycharmProjects\pythonProject\LargeCap_scan_list02.csv', sep=';') #mid capet és lc-t összerakni.. backtest midcappel is
    contracts = scan['Symbol'].tolist()
    getData(contracts, defaultid, scan)
    app.data = []
    print('updating_data')
    print(datetime.now().strftime('%H:%M:%S'))
    df0 = read_csv(r'C:\Users\user\PycharmProjects\pythonProject\trading_list_datas.csv')
    prepare_data_into_individual_frames(df0)
    strategy_calculation_for_all_symbol()
    print(buy_signal_list)


running()

