# %%

from __future__ import print_function
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)
import time
import threading
import os
from operator import itemgetter

# %%

binance_websocket_api_manager = BinanceWebSocketApiManager(output_default="UnicornFy")


markets = ["btcusdt", "ethusdt"]

channels = ["kline_15m"]

for market in markets:
    binance_websocket_api_manager.create_stream(
        channels, market, stream_buffer_name=market + "_15m"
    )

# %%

data_dict = {mkt + "_15m": [] for mkt in markets}
# %%

for channel in channels:
    binance_websocket_api_manager.create_stream(
        channel, markets, stream_buffer_name=channel
    )


def print_stream_data_from_stream_buffer(binance_websocket_api_manager, symbol):
    print("print trades only")
    time.sleep(4)
    while True:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        oldest_stream_data_from_stream_buffer = (
            binance_websocket_api_manager.pop_stream_data_from_stream_buffer(symbol)
        )
        if oldest_stream_data_from_stream_buffer is False:
            time.sleep(0.01)
        else:
            try:
                data = itemgetter("symbol", "close_price")(
                    oldest_stream_data_from_stream_buffer["kline"]
                )
                data_dict[symbol].append(data)
                # print(data)
            except Exception:
                # not able to process the data? write it back to the stream_buffer
                binance_websocket_api_manager.add_to_stream_buffer(
                    oldest_stream_data_from_stream_buffer
                )


# %%

# start a worker process to process to move the received stream_data from the stream_buffer to a print function
def new_thread(symbol):
    """
    Docstring for new_thread
    """
    worker_thread = threading.Thread(
        target=print_stream_data_from_stream_buffer,
        args=(
            binance_websocket_api_manager,
            symbol,
        ),
    )
    worker_thread.start()
    return worker_thread


# %%
thread2 = new_thread("ethusdt_15m")
# %%

thread1 = new_thread("btcusdt_15m")


# %%
data_dict["btcusdt_15m"]
# %%
data_dict["ethusdt_15m"]
