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


def to_percentual(exit_price, entry_price, leverage=1):
    """
    Converts a difference in values to a percentual difference.

    Args:
        exit_price (float or integer)
        entry_price (float or integer)
        leverage (int)
    Returns:
        float: ((exit_price - entry_price) / entry_price) * 100 * leverage
    """
    return ((exit_price - entry_price) / entry_price) * 100 * leverage


UTCM3 = -pd.Timedelta("3:00:00")


def to_datetime_tz(arg, timedelta=-pd.Timedelta("03:00:00"), unit="s", **kwargs):
    """
    to_datetime_tz(arg, timedelta=-pd.Timedelta("03:00:00"), unit="s", **kwargs)

    Args:
        arg (float): epochtime
        timedelta (pd.Timedelta): timezone correction
        unit (string): unit in which `arg` is
        **kwargs: pd.to_datetime remaining kwargs
    Returns:
    pd.Timestamp: a timestamp corrected by the given timedelta
    """
    ts = pd.to_datetime(arg, unit=unit)
    return ts + timedelta


def strf_epoch(epochtime, fmt="%j.%y_%H-%M-%S"):
    """




    returns: string
    """

    """
    epochtime to string using datetime
    signature: def strf_epoch(epochtime, fmt="%j.%y_%H-%M-%S")

    Args:
        epochtime (float): epochtime as float in seconds
        fmt (string): format for the timestamp string
    Returns:
        string: stringfied epochtime: datetime.fromtimestamp(epochtime).strftime(fmt)
    """

    return datetime.fromtimestamp(epochtime).strftime(fmt)


# LOGGER CONFIG
LOG_DATEFORMAT = "%j.%y_%H-%M-%S"

if not os.path.exists("logs/"):
    os.mkdir("logs/")

logs_for_this_run = f"logs/{strf_epoch(time.time())}/"

if not os.path.exists(logs_for_this_run):
    os.mkdir(logs_for_this_run)

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


# import logging
# import csv
# import io
#
#
# class CsvFormatter(logging.Formatter):
#     def __init__(self):
#         super().__init__()
#         self.output = io.StringIO()
#         self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)
#
#     def format(self, record):
#         self.writer.writerow([record.levelname, record.msg])
#         data = self.output.getvalue()
#         self.output.truncate(0)
#         self.output.seek(0)
#         return data.strip()
#
#
# logging.basicConfig(level=logging.DEBUG)
#
# logger = logging.getLogger(__name__)
# logging.root.handlers[0].setFormatter(CsvFormatter())
#
# logger.debug("This message should appear on the console")
# logger.info('So should "this", and it\'s using quoting...')
# logger.warning("And this, too")
