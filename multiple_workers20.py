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


class Manager:
    def __init__(self):
        self.traders = {}
        self.bwsm = BinanceWebSocketApiManager(output_default="UnicornFy")

    def start_trader(self):
        trader = ATrader(self)
        trader.start_new_stream()
        self.traders[trader.stream_name]["trader"] = trader

    def get_traders(self):
        return list(self.traders.values())


# %%


class ATrader:
    def __init__(self, manager):
        self.manager = manager
        self.bwsm = manager.bwsm
        self.data = self.manager.traders
        self.keep_running = True
        self.stream_id = None
        self.stream_name = None

    def process_stream_data(self, stream_id):

        while self.keep_running:
            if self.bwsm.is_manager_stopping():
                exit(0)
            oldest_stream_data_from_stream_buffer = (
                self.bwsm.pop_stream_data_from_stream_buffer(stream_id)
            )
            if oldest_stream_data_from_stream_buffer is False:
                time.sleep(0.01)
            else:
                self.data[self.stream_name]["data"].append(
                    oldest_stream_data_from_stream_buffer
                )

    def start_new_stream(self):

        stream_name = "bookTicker" + "@" + "bnbusd"

        book_ticker_id = self.bwsm.create_stream(
            "bookTicker", "bnbbusd", stream_buffer_name=stream_name
        )

        worker = threading.Thread(
            target=self.process_stream_data, args=(book_ticker_id,)
        )
        worker.start()
        self.data[stream_name] = {"trader": None, "data": []}
        self.stream_name = stream_name
        self.worker = worker
        self.stream_id = book_ticker_id

    def stop(self):
        self.keep_running = False
        self.bwsm.stop_stream(self.stream_id)


# %%
manager = Manager()
# %%
manager.start_trader()

# %%
manager.traders
# %%
manager.traders["bookTicker@bnbusd"]["data"]
# atrader = ATrader(manager.bwsm)
# %%
# worker = atrader.start_new_stream()
# %%
manager.traders["bookTicker@bnbusd"]
# %%
atrader.data

# %%
