
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import pandas
from pandas import *

scan = read_csv("Sickle.csv")
scan.to_csv(f'C:\\Users\\user\\PycharmProjects\\pythonProject\\'
               f'Sickle.csv', index=False, sep=';')