from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)
import logging
import os
import requests
import sys
import time
import threading

try:
    import unicorn_binance_rest_api
except ImportError:
    print(
        "Please install `unicorn-binance-rest-api`! https://pypi.org/project/unicorn-binance-rest-api/"
    )
    sys.exit(1)

try:
    import IPython
except ImportError:
    print("Please install `jupyter`! https://ipython.org/")
    sys.exit(1)

# https://docs.python.org/3/library/logging.html#logging-levels
logging.basicConfig(
    level=logging.INFO,
    filename=os.path.basename(__file__) + ".log",
    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
    style="{",
)


def print_stream_data_from_stream_buffer(binance_websocket_api_manager):
    while True:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        oldest_stream_data_from_stream_buffer = (
            binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        )
        if oldest_stream_data_from_stream_buffer is not False:
            pass
        else:
            time.sleep(0.01)


def print_stream(manager):
    while True:
        manager.print_summary(disable_print=True)
        time.sleep(10)


channels = {
    "aggTrade",
    "trade",
    "kline_1m",
    "kline_5m",
    "kline_15m",
    "kline_30m",
    "kline_1h",
    "kline_2h",
    "kline_4h",
    "kline_6h",
    "kline_8h",
    "kline_12h",
    "kline_1d",
    "kline_3d",
    "kline_1w",
    "kline_1M",
    "miniTicker",
    "ticker",
    "bookTicker",
    "depth5",
    "depth10",
    "depth20",
    "depth",
    "depth@100ms",
}
arr_channels = {"!miniTicker", "!ticker", "!bookTicker"}
markets = []

try:
    binance_api_key = ""
    binance_api_secret = ""
    binance_rest_client = unicorn_binance_rest_api.BinanceRestApiManager(
        binance_api_key, binance_api_secret
    )
    binance_websocket_api_manager = BinanceWebSocketApiManager()
except requests.exceptions.ConnectionError:
    print("No internet connection?")
    sys.exit(1)

# start a worker process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(
    target=print_stream_data_from_stream_buffer, args=(binance_websocket_api_manager,)
)
worker_thread.start()

print_summary_thread = threading.Thread(
    target=print_stream, args=(binance_websocket_api_manager,)
)
print_summary_thread.start()

data = binance_rest_client.get_all_tickers()
for item in data:
    markets.append(item["symbol"])

binance_websocket_api_manager.create_stream(
    ["!userData"], ["arr"], "Alice userData stream", api_key="aaa", api_secret="bbb"
)
binance_websocket_api_manager.create_stream(
    ["!userData"], ["arr"], "Bobs userData stream", api_key="ccc", api_secret="ddd"
)

binance_websocket_api_manager.create_stream(
    arr_channels, "arr", stream_label="arr channels"
)

for channel in channels:
    binance_websocket_api_manager.create_stream(channel, markets, stream_label=channel)

ubwa = binance_websocket_api_manager

IPython.embed()
