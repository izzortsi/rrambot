##
import os
import time
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
##
data = []
def btc_trade_history(msg):
    ''' define how to process incoming WebSocket messages '''
    if msg['e'] != 'error':
        global data
        data.append(msg["k"])
        print(data[-1])
##
client=Client()
##
bsm = BinanceSocketManager(client)
##
btc_ckey = bsm.start_kline_socket('BTCUSDT', btc_trade_history)
bsm.start()
##
eth_ckey = bsm.start_kline_socket('ETHUSDT', btc_trade_history)
##
bsm.close()
##
reactor.stop()
