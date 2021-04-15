##
from binance.client import Client
from binance.websockets import BinanceSocketManager
from grabber import *
##
def process_message(msg):
    print(msg[0]["c"])
##
client=Client()
bm = BinanceSocketManager(client)
# start any sockets here, i.e a trade socket
#conn_key = bm.start_kline_socket('BNBBTC', process_message, interval="1m")
# then start the socket manager
#bm.start()
##
conn_key = bm.start_miniticker_socket(process_message)
bm.start()
##
bm.close()
##
class ATrader:

    def __init__(self):

