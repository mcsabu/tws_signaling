from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import pandas
from pandas import *


scan = read_csv("md_runnerek2021_2022_prem.csv", sep=';')
scan = scan[135:150]


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
app.connect('127.0.0.1', 7496, 10)

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)  # Sleep interval to allow time for connection to server


#printed_symbol = []

defaultid = 0
def getData(contracts, defaultid):
    for i in contracts:
        symbol = i
        fileName = i

        defaultid += 1

        #printed_symbol.append(symbol)
        #printed_symbol.append(defaultid)
        duration = '2 Y'
        resolution = '5 mins'

        print('Ticker: '+ fileName + ' ')
        print('Downloading...')
        #print(printed_symbol)
        #Create contract object
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'

        app.reqHistoricalData(defaultid, contract, '', duration, resolution, 'TRADES', 0, 2, False, [])

        time.sleep(700)  # sleep to allow enough time for data to be returned




        df = pandas.DataFrame(app.data, columns=['reqID', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        df['Date'] = pandas.to_datetime(df['Date'], unit='s')

        df.Volume *= 100 #100 lotként küldi az IB a volume-ot



        df = pandas.merge(scan, df, on='reqID')
        print(df.head(1), df.tail(1))
        #to_csv(..., sep=';')
        df.to_csv(f'C:\\Users\\user\\PycharmProjects\\pythonProject\\'
               f'Micro_List_2Y_5m_prem_part10.csv', index=False, sep=';')



getData(contracts, defaultid)




app.disconnect()

