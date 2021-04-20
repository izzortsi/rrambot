#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_multi_stream.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api
# Documentation: https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: Oliver Zehentleitner
#         https://about.me/oliver-zehentleitner
#
# Copyright (c) 2019-2021, Oliver Zehentleitner
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# %%
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)
import logging
import os
import time

# %%
# import class to process stream data
from process_streams import BinanceWebSocketApiProcessStreams

# create instance of BinanceWebSocketApiManager and provide the function for stream processing
binance_websocket_api_manager = BinanceWebSocketApiManager()
# %%
# define markets
markets = ["ethusdt", "btcusdt"]
# %%
# define stream channels
channels = ["kline_1", "kline_15"]
# %%
# create and start the stream
# %%
def print_stream(stream_id, data, n=10):
    label = binance_websocket_api_manager.get_stream_label(eth_id)
    c = 0
    while c <= n:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        oldest_stream_data_from_stream_buffer = (
            binance_websocket_api_manager.pop_stream_data_from_stream_buffer(
                stream_buffer_name=label
            )
        )
        if oldest_stream_data_from_stream_buffer is False:
            time.sleep(0.01)
        else:
            if oldest_stream_data_from_stream_buffer is not None:
                try:
                    if (
                        oldest_stream_data_from_stream_buffer["event_time"]
                        >= oldest_stream_data_from_stream_buffer["kline"][
                            "kline_close_time"
                        ]
                    ):
                        # print only the last kline
                        data.append(oldest_stream_data_from_stream_buffer)
                        print(f"UnicornFy: {oldest_stream_data_from_stream_buffer}")
                except KeyError:
                    print(f"dict: {oldest_stream_data_from_stream_buffer}")
                except TypeError:
                    print(f"raw_data: {oldest_stream_data_from_stream_buffer}")

        c += 1


# %%

# %%
eth_id = binance_websocket_api_manager.create_stream(
    channels[0], markets[0], output="UnicornFy", stream_label="ethusdt_1m"
)
# %%
btc_id = binance_websocket_api_manager.create_stream(
    "kline_1", "btcusdt", output="UnicornFy"
)
# binance_websocket_api_manager.print_stream_info(eth_id)
# %%
data = []
print_stream(btc_id, data, n=10000)

# %%
data
# %%
# stop the stream
binance_websocket_api_manager.stop_stream(eth_id)
time.sleep(3)
# %%
# print info about the stream
print("\r\n\r\n")
binance_websocket_api_manager.print_stream_info(multi_stream_id)
# %%
print(
    "\r\n=============================== Stopping BinanceWebSocketManager ======================================\r\n"
)
binance_websocket_api_manager.stop_manager_with_all_streams()
print("finished!")
# %%
