import json
import logging
import os
import time
import threading
import numpy as np
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
from urllib.parse import urlencode
from auxs import *

from unicorn_binance_rest_api.unicorn_binance_rest_api_manager import (
    BinanceRestApiManager as Client,
)
from unicorn_binance_rest_api.unicorn_binance_rest_api_helpers import (
    interval_to_milliseconds,
)
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)

# CONSTANTS

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
UTCM3 = -pd.Timedelta("3:00:00")

# AUXILIARY FUNCTIONS


def futures_mark_price_klines(self, **params):
    """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.
    https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-data-market_data
    """
    return self._request_futures_api("get", "markPriceKlines", data=params)


def futures_place_batch_order(self, **params):
    """Send in new orders.
    https://binance-docs.github.io/apidocs/delivery/en/#place-multiple-orders-trade
    To avoid modifying the existing signature generation and parameter order logic,
    the url encoding is done on the special query param, batchOrders, in the early stage.
    """
    query_string = urlencode(params)
    query_string = query_string.replace("%27", "%22")
    params["batchOrders"] = query_string[12:]
    return self._request_futures_api("post", "batchOrders", True, data=params)


Client.futures_mark_price_klines = futures_mark_price_klines
Client.futures_place_batch_order = futures_place_batch_order

# LOGGER CONFIG

LOG_DATEFORMAT = "%j-%y_%H-%M-%S"

if not os.path.exists("logs"):
    os.mkdir("logs")

logs_for_this_run = os.path.join("logs", strf_epoch(time.time()))

if not os.path.exists(logs_for_this_run):
    os.mkdir(logs_for_this_run)

formatter = logging.Formatter("%(asctime)s %(message)s")


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
