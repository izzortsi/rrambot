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

bwsm = BinanceWebSocketApiManager(output_default="UnicornFy")


markets = ["btcusdt", "ethusdt"]
names = [mkt + "_15m" for mkt in markets]
channels = ["kline_15m"]

for market in markets:
    bwsm.create_stream(channels, market, stream_buffer_name=market + "_15m")

# %%
data_dict = {name: [] for name in names}
# %%


def print_stream_data_from_stream_buffer(bwsm, stream_name):
    print("print trades only")
    time.sleep(4)
    while True:
        if bwsm.is_manager_stopping():
            exit(0)
        oldest_stream_data_from_stream_buffer = bwsm.pop_stream_data_from_stream_buffer(
            stream_name
        )
        if oldest_stream_data_from_stream_buffer is False:
            time.sleep(0.01)
        else:
            try:
                data = itemgetter("symbol", "close_price")(
                    oldest_stream_data_from_stream_buffer["kline"]
                )
                data_dict[stream_name].append(data)
                # print(data)
            except Exception:
                # not able to process the data? write it back to the stream_buffer
                bwsm.add_to_stream_buffer(oldest_stream_data_from_stream_buffer)


# %%

# start a worker process to process to move the received stream_data from the stream_buffer to a print function
def new_thread(bwsm, stream_name):
    """
    Docstring for new_thread
    """
    worker_thread = threading.Thread(
        target=print_stream_data_from_stream_buffer,
        args=(
            bwsm,
            stream_name,
        ),
    )
    worker_thread.start()
    return worker_thread


# %%
thread2 = new_thread(bwsm, "ethusdt_15m")
# %%

thread1 = new_thread(bwsm, "btcusdt_15m")


# %%
data_dict["btcusdt_15m"]
# %%
data_dict["ethusdt_15m"]
