# %%
import os
import time
import threading
import numpy as np
import pandas as pd
from grabber import DataGrabber

from unicorn_binance_rest_api.unicorn_binance_rest_api_manager import (
    BinanceRestApiManager as Client,
)

from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)
from unicorn_binance_rest_api.unicorn_binance_rest_api_helpers import (
    interval_to_milliseconds,
)

from operator import itemgetter

# %%

api_key = ""
api_secret = ""


api_key = ""
api_secret = ""


def book_ticker(msg):
    print("book_ticker: " + str(msg))


def order_status(msg):
    print("order_status: " + str(msg))


book_ticker_id = bwsm.create_stream("bookTicker", "bnbbusd", stream_buffer_name=True)
user_stream_id = bwsm.create_stream(
    "arr", "!userData", api_key=api_key, api_secret=api_secret, stream_buffer_name=True
)

while True:
    msg = bwsm.pop_stream_data_from_stream_buffer(book_ticker_id)
    if msg:
        book_ticker(msg)
    msg = bwsm.pop_stream_data_from_stream_buffer(user_stream_id)
    if msg:
        order_status(msg)
    time.sleep(0.01)


class Manager:
    def __init__(self):
        self.traders = {}
        self.bwsm = BinanceWebSocketApiManager()

    def start_trader(self):

        trader = ATrader(self, self.bwsm)
        self.traders[trader.name] = trader


# %%


class ATrader:
    def __init__(self, bwsm):

        self.bwsm = bwsm
        self.data = []
        self.keep_running = True

    def process_stream_data_from_stream_buffer(self, stream_name):

        time.sleep(1)

        c = 0
        while self.keep_running:
            if self.bwsm.is_manager_stopping():
                exit(0)
            oldest_stream_data_from_stream_buffer = (
                self.bwsm.pop_stream_data_from_stream_buffer(stream_name)
            )
            if oldest_stream_data_from_stream_buffer is False:
                time.sleep(0.01)
            else:
                try:
                    print(oldest_stream_data_from_stream_buffer)
                    data = itemgetter(
                        "symbol", "close_price", "base_volume", "is_closed"
                    )(oldest_stream_data_from_stream_buffer["kline"])
                    self.data.append(data)
                    if c % 5 == 0:
                        print(data)

                except Exception:
                    # not able to process the data? write it back to the stream_buffer
                    self.bwsm.add_to_stream_buffer(
                        oldest_stream_data_from_stream_buffer
                    )
            c += 1

    def start_new_stream(self, channel, market, stream_name=None):

        if stream_name is None:
            stream_name = market + "_" + channel

        stream_name = self.bwsm.create_stream(
            channel,
            market,
        )

        worker = threading.Thread(
            target=self.process_stream_data_from_stream_buffer, args=(stream_name,)
        )
        worker.start()
        return stream_name, worker

    def stop(self):
        self.keep_running = False
        self.bwsm.stop_stream(self.stream_name)


# %%
manager = Manager(api_key, api_secret)
# %%
atrader = ATrader(manager.bwsm)
# %%
stream_name, worker = atrader.start_new_stream("kline_15m", "btcusdt")
# %%
stream_name
manager.bwsm.get_active_stream_list()
# %%
atrader.data
# %%

# %%
