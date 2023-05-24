from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import pandas
from pandas import *


scan = read_csv("LargeCap_scan_list.csv", sep=';')
scan = scan[500:750]


contracts = scan['Symbol'].tolist()

print(scan)

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []  # Initialize variable to store candle

    def historicalData(self, reqId, bar):
        #print("{},{},{},{},{},{}"
        #.format(bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume))
        self.data.append([reqId, bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])


def run_loop():
    app.run()

app = IBapi()
app.connect('127.0.0.1', 7496, 100)

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)  # Sleep interval to allow time for connection to server


defaultid = 0
def getData(contracts, defaultid):
    for i in contracts:
        symbol = i
        fileName = i

        defaultid += 1

        duration = '20 Y'
        resolution = '1 day'

        print('Ticker: '+ fileName + ' ')
        print('Downloading...')

        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'

        app.reqHistoricalData(defaultid, contract, '', duration, resolution, 'TRADES', 1, 2, False, [])

        time.sleep(5)  # sleep to allow enough time for data to be returned
        try:
            df = pandas.DataFrame(app.data, columns=['reqID', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['Date'] = pandas.to_datetime(df['Date'])

            df.Volume *= 100 #100 lotként küldi az IB a volume-ot

            df = pandas.merge(scan, df, on='reqID')
            print(df.head(1), df.tail(1))
            #to_csv(..., sep=';')
            df.to_csv(r'C:\Users\user\PycharmProjects\pythonProject\LargeCap_List_20Y_1D_part3.csv', sep=';')
        except ValueError:
            pass

getData(contracts, defaultid)

app.disconnect()

