from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import pandas
from pandas import *


scan = read_csv("LargeCap.csv")
contracts = scan['Symbol'].tolist()