
##
import os
import time
from binance.client import Client
from binance.websockets import BinanceSocketManager
from multiprocessing import Process, Queue
from twisted.internet import reactor
#from grabber import GrabberMACD, Grabber
##

client = Client()
##
#grabmacd = GrabberMACD(client)
#grab = Grabber(client)

##
#grabmacd.get_data(symbol="BTCUSDT", tframe="1m", fromdate="1 day ago", todate = None)
#grabmacd.trim_data()
#df = grabmacd.compute_indicators()
##
class Manager:
    
    def __init__(self, api_key=None, api_secret=None):
        self.client = Client(api_key = api_key, api_secret=api_secret)
        self.bsm = BinanceSocketManager(self.client)
        self.traders = {}
        self.trading = []

    def add_trader(self, strategy, init_val, symbol, timeframe):
        socket = self.bsm.start_kline_socket(symbol, self.process_message, interval=timeframe)
        name = f"{symbol}_{timeframe}_{strategy.name}"
        atrader = ATrader(name, self, strategy, socket, init_val, symbol, timeframe)
        self.traders[name] = atrader

    def process_message(self, msg):
        ''' define how to process incoming WebSocket messages '''
        if msg['e'] != 'error':
            print(msg['k']["c"])
            self.exitprices.append(msg['k']["c"])
        else:
            self.socket_error = True

    def remove_trader(self, name = None, conditions = None):
        #remove um trader diretamente pelo nome ou por condiçoes (como determiná-las?)
        raise NotImplementedError

    def get_traders(self):
        print(self.traders.keys)
        return self.traders


class ATrader:

    def __init__(self, name, manager, socket, strategy, init_val, symbol, timeframe):

        self.strategy = strategy
        self.name = name
        self.init_val = init_val
        self.symbol = symbol
        self.timeframe = timeframe
        self.state = False
        
        self.manager = manager
        self.socket = socket
        self.socket_error = False

        self.entrydates = []
        self.exitdates = []
        self.entryprices = []
        self.exitprices = []

        self.log = []
        self.profits = []

    def trade(self, i, dates, prices, indicators):
        self.manager.running.append(name)
        pass


##
trader = ATrader("strategy", 0.1, "BTCUSDT", "1m")

##
trader.connect()
##
trader.exitprices
##
trader.disconnect()

##
trader2 = ATrader("strategy", 0.1, "BTCUSDT", "1m")
##
trader2.connect()
##
reactor.stop()
##
def kill(trader):
    trader.bsm.close(trader.conn_key)
    reactor.stop()

##
kill(trader)
##
##
def btc_trade_history(msg):
    ''' define how to process incoming WebSocket messages '''
    if msg['e'] != 'error':
        global data
        
        data.append(msg["k"])
        print(data[-1])


##

bsm = BinanceSocketManager(client)
conn_key = bsm.start_kline_socket('BTCUSDT', btc_trade_history)
bsm.start()
##
time.sleep(10)
##
bsm.close()
reactor.stop()
##
tick = {'t': 1618600560000, 'T': 1618600619999, 's': 'BTCUSDT', 'i': '1m', 'f': 770761568, 'L': 770762621, 'o': '61758.79000000', 'c': '61749.96000000', 'h': '61760.69000000', 'l': '61710.02000000', 'v': '18.37346200', 'n': 1054, 'x': False, 'q': '1134320.28513451', 'V': '5.33180600', 'Q': '329177.71258439', 'B': '0'}
##
type(tick["t"])
##
grabmacd.klines[-1]
##
