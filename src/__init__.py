import logging
import os
import time
import threading
import numpy as np
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

# AUXILIARY FUNCTIONS


def futures_mark_price_klines(self, **params):
    """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.
    https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-data-market_data
    """
    return self._request_futures_api("get", "markPriceKlines", data=params)


Client.futures_mark_price_klines = futures_mark_price_klines


def name_trader(strategy, symbol):
    return "_".join([strategy.name, symbol, strategy.timeframe])


def to_percentual(exit_price, entry_price):
    return ((exit_price - entry_price) / entry_price) * 100


# LOGGER CONFIG

if not os.path.exists("logs/"):
    os.mkdir("logs/")

# %%

formatter = logging.Formatter("%(asctime)s %(message)s")


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
