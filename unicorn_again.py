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
        else:
            print(oldest_stream_data_from_stream_buffer)


# configure api key and secret for binance.com
binance_com_api_key = os.environ.get("API_KEY")
binance_com_api_secret = os.environ.get("API_SECRET")

# configure api key and secret for binance.je

# create instances of BinanceWebSocketApiManager
binance_com_websocket_api_manager = BinanceWebSocketApiManager(
    exchange="binance.com", throw_exception_if_unrepairable=True
)
# create the userData streams
binance_com_user_data_stream_id = binance_com_websocket_api_manager.create_stream(
    "arr", "!userData", api_key=binance_com_api_key, api_secret=binance_com_api_secret
)


# start a worker process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(
    target=print_stream_data_from_stream_buffer,
    args=(binance_com_websocket_api_manager,),
)
worker_thread.start()


# monitor the streams
while True:

    binance_com_websocket_api_manager.print_summary()
    time.sleep(5)
