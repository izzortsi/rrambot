# %%
# %%
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)
import logging
import os
import sys
import time
import threading
from dataclasses import dataclass
from unicorn_fy.unicorn_fy import UnicornFy

import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.stats
import pandas as pd
import pandas_ta as ta

# %%
@dataclass
class SymbolData:
    market: str = ""
    channel: str = ""
    name: str = ""
    data: list = None

    def __repr__(self):
        return f"{self.name}@{self.channel}"


# %%

# %%
sym = SymbolData()
sym.data = []


# %%
class BinanceWebSocketApiProcessStreams(object):
    @staticmethod
    def process_stream_data(
        received_stream_data_json,
        exchange="binance.com-futures",
        stream_buffer_name="False",
    ):
        #
        #  START HERE!
        #
        # `received_stream_data_json` contains one record of raw data from the stream
        # print it and you see the data like its given from Binance, its hard to work with them, because keys of
        # parameters are changing from stream to stream and they are not self explaining.
        #
        # So if you want, you can use the class `UnicornFy`, it converts the json to a dict and prepares the values.
        # `depth5` for example doesnt include the symbol, but the unicornfied set includes them, because the class
        # extracts it from the channel name, makes it upper size and adds it to the returned values.. just print both
        # to see the difference.
        # Github: https://github.com/oliver-zehentleitner/unicorn-fy
        # PyPI: https://pypi.org/project/unicorn-fy/
        if exchange == "binance.com" or exchange == "binance.com-testnet":
            unicorn_fied_stream_data = UnicornFy.binance_com_websocket(
                received_stream_data_json
            )
        elif (
            exchange == "binance.com-futures"
            or exchange == "binance.com-futures-testnet"
        ):
            unicorn_fied_stream_data = UnicornFy.binance_com_futures_websocket(
                received_stream_data_json
            )
        elif (
            exchange == "binance.com-margin" or exchange == "binance.com-margin-testnet"
        ):
            unicorn_fied_stream_data = UnicornFy.binance_com_margin_websocket(
                received_stream_data_json
            )
        elif (
            exchange == "binance.com-isolated_margin"
            or exchange == "binance.com-isolated_margin-testnet"
        ):
            unicorn_fied_stream_data = UnicornFy.binance_com_margin_websocket(
                received_stream_data_json
            )
        elif exchange == "binance.je":
            unicorn_fied_stream_data = UnicornFy.binance_je_websocket(
                received_stream_data_json
            )
        elif exchange == "binance.us":
            unicorn_fied_stream_data = UnicornFy.binance_us_websocket(
                received_stream_data_json
            )
        else:
            logging.error("Not a valid exchange: " + str(exchange))

        # Now you can call different methods for different `channels`, here called `event_types`.
        # Its up to you if you call the methods in the bottom of this file or to call other classes which do what
        # ever you want to be done.
        try:
            if unicorn_fied_stream_data["event_type"] == "aggTrade":
                BinanceWebSocketApiProcessStreams.aggtrade(unicorn_fied_stream_data)
            elif unicorn_fied_stream_data["event_type"] == "trade":
                BinanceWebSocketApiProcessStreams.trade(unicorn_fied_stream_data)
            elif unicorn_fied_stream_data["event_type"] == "kline":
                BinanceWebSocketApiProcessStreams.kline(unicorn_fied_stream_data)
            elif unicorn_fied_stream_data["event_type"] == "24hrMiniTicker":
                BinanceWebSocketApiProcessStreams.miniticker(unicorn_fied_stream_data)
            elif unicorn_fied_stream_data["event_type"] == "24hrTicker":
                BinanceWebSocketApiProcessStreams.ticker(unicorn_fied_stream_data)
            elif unicorn_fied_stream_data["event_type"] == "depth":
                BinanceWebSocketApiProcessStreams.miniticker(unicorn_fied_stream_data)
            else:
                BinanceWebSocketApiProcessStreams.anything_else(
                    unicorn_fied_stream_data
                )
        except KeyError:
            BinanceWebSocketApiProcessStreams.anything_else(unicorn_fied_stream_data)
        except TypeError:
            pass

    @staticmethod
    def aggtrade(stream_data):
        # print `aggTrade` data
        # print(stream_data)
        # time.sleep(10)
        pass

    @staticmethod
    def trade(stream_data):
        # print `trade` data
        # print(stream_data)
        # time.sleep(10)
        pass

    @staticmethod
    def kline(stream_data):
        # print `kline` data
        # print(stream_data)
        # time.sleep(10)
        global sym
        sym.data.append(stream_data)
        time.sleep(5)
        # print(threading.activeCount())

    @staticmethod
    def miniticker(stream_data):
        # print `miniTicker` data
        # print(stream_data)
        # time.sleep(10)
        pass

    @staticmethod
    def ticker(stream_data):
        # print `ticker` data
        # print(stream_data)
        # time.sleep(10)
        pass

    @staticmethod
    def depth(stream_data):
        # print `depth` data
        # print(stream_data)
        # time.sleep(10)
        pass

    @staticmethod
    def outboundAccountInfo(stream_data):
        # print `outboundAccountInfo` data from userData stream
        # print(stream_data)
        # time.sleep(10)
        pass

    @staticmethod
    def executionReport(stream_data):
        # print `executionReport` data from userData stream
        # print(stream_data)
        # time.sleep(10)
        pass

    @staticmethod
    def anything_else(stream_data):
        # print(stream_data)
        # time.sleep(10)
        pass


# https://docs.python.org/3/library/logging.html#logging-levels

# create instance of BinanceWebSocketApiManager and provide the function for stream processing
binance_websocket_api_manager = BinanceWebSocketApiManager(
    BinanceWebSocketApiProcessStreams.process_stream_data,
    exchange="binance.com-futures",
)

# define markets
markets = {
    "btcusdt",
    "bchabcusdt",
    "xrpusdt",
    "ltcusdt",
    "adausdt",
    "eosusdt",
    "neousdt",
    "bnbusdt",
    "ethusdt",
    "bttusdt",
    "tusdusdt",
    "xlmusdt",
    "adaeth",
    "icxusdt",
    "zrxusdt",
}

# define stream channels
channels = {
    "trade",
    "kline_1",
    "kline_5",
    "kline_15",
    "kline_30",
    "kline_1h",
    "kline_12h",
    "kline_1w",
    "miniTicker",
}
# %%
threading.active_count()

# create and start the stream
print("please wait 10 seconds!")
time.sleep(3)
multi_stream_id = binance_websocket_api_manager.create_stream(channels, markets)
binance_websocket_api_manager.get_stream_subscriptions(multi_stream_id)
binance_websocket_api_manager.print_stream_info(multi_stream_id)
# time.sleep(10)

# stop the stream
# binance_websocket_api_manager.stop_stream(multi_stream_id)
# time.sleep(3)

# print info about the stream
# print("\r\n\r\n")
# binance_websocket_api_manager.print_stream_info(multi_stream_id)
# time.sleep(30)
# print(
#     "\r\n=============================== Stopping BinanceWebSocketManager ======================================\r\n"
# )
# binance_websocket_api_manager.stop_manager_with_all_streams()
# print("finished!")
