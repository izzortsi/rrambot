# %%
import os
import time
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor

# %%
databtc = []
dataeth = []
# %%


def btc_trade_history(msg):
    """ define how to process incoming WebSocket messages """
    if msg["e"] != "error":
        global databtc
        databtc.append(msg["k"])
        print(databtc[-1])


def eth_trade_history(msg):
    """ define how to process incoming WebSocket messages """
    if msg["e"] != "error":
        global dataeth
        dataeth.append(msg["k"])
        print(dataeth[-1])


# %%
client = Client()
# %%
# bsm = BinanceSocketManager(client)
bsm = BinanceMul(client)
# %%
btc_ckey = bsm.start_kline_socket("BTCUSDT", btc_trade_history)
bnb_ckey = bsm.start_kline_socket("ETHUSDT", eth_trade_history)
# %%
databtc
##
dataeth
# %%
bsm.start()
# %%
bnb_ckey = bsm.start_kline_socket("BNBUSDT", btc_trade_history)
eth_ckey = bsm.start_kline_socket("ETHUSDT", btc_trade_history)
# %%
bsm.close()
# %%
reactor.stop()
