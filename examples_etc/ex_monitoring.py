from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)
import logging
import time
import threading
import os

# https://docs.python.org/3/library/logging.html#logging-levels


def print_stream_data_from_stream_buffer(binance_websocket_api_manager):
    while True:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        oldest_stream_data_from_stream_buffer = (
            binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        )
        if oldest_stream_data_from_stream_buffer is False:
            time.sleep(0.01)


# create instance of BinanceWebSocketApiManager for Binance.com Futures
binance_websocket_api_manager = BinanceWebSocketApiManager(
    exchange="binance.com-futures"
)

# https://binance-docs.github.io/apidocs/futures/en/#mark-price-stream-for-all-market
stream_id = binance_websocket_api_manager.create_stream(
    ["!markPrice"], "arr@1s", stream_label="!markPrice@arr@1s"
)

# start a worker process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(
    target=print_stream_data_from_stream_buffer, args=(binance_websocket_api_manager,)
)
worker_thread.start()


time.sleep(5)
binance_websocket_api_manager.get_stream_subscriptions(stream_id)
time.sleep(3)
print(str(binance_websocket_api_manager.get_results_from_endpoints()))
time.sleep(5)
# show an overview
while True:
    binance_websocket_api_manager.print_stream_info(stream_id)
    time.sleep(1)
