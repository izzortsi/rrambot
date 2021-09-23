# %%

from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)
from semiauto.process_stream import BinanceWebSocketApiProcessStreams
import logging
import os
import requests
import sys
import time
import threading

# %%


if "__name__" == __main__:

    pstreams = BinanceWebSocketApiProcessStreams()
    bws = BinanceWebSocketApiManager(
        process_stream_data=pstreams.ticker,
        exchange="binance.com-futures",
        output_default="unicorn-fy",
    )
    bws.create_stream(
        "!ticker",
        "arr",
        stream_label="!ticker@arr",
        stream_buffer_name="!ticker@arr",
        ping_interval=10,
        ping_timeout=10,
        close_timeout=5,
    )
