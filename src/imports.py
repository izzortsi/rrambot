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
import tradingview_ta

from symbols_formats import FORMATS
from datetime import datetime
from urllib.parse import urlencode
from tradingview_ta import TA_Handler, Interval, Exchange, get_multiple_analysis
from unicorn_binance_rest_api.unicorn_binance_rest_api_exceptions import *
from src.symbols_formats import FORMATS

from unicorn_binance_rest_api.unicorn_binance_rest_api_manager import (
    BinanceRestApiManager as Client,
)
from unicorn_binance_rest_api.unicorn_binance_rest_api_helpers import (
    interval_to_milliseconds,
)
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)


# %%

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

tframes = ["5m", "15m", "1h"]

coins = ["eth", "ada", "bnb", "xrp", "doge", "dot", "xlm", "iota", "dash"]

symbols_tv = [f"binance:{coin}usdt" for coin in coins]


# %%

# CONSTANTS

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
UTCM3 = -pd.Timedelta("3:00:00")

# AUXILIARY FUNCTIONS

substring_check = np.frompyfunc((lambda s, array: s in array), 2, 1)


def side_from_int(self):
    if self.position_type == -1:
        return "SELL", "BUY"
    elif self.position_type == 1:
        return "BUY", "SELL"


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


def strf_epoch(epochtime, fmt="%j-%y_%H-%M-%S"):
    """
    returns: string
    """

    """
    epochtime to string using datetime
    signature: def strf_epoch(epochtime, fmt="%j-%y_%H-%M-%S")

    Args:
        epochtime (float): epochtime as float in seconds
        fmt (string): format for the timestamp string
    Returns:
        string: stringfied epochtime: datetime.fromtimestamp(epochtime).strftime(fmt)
    """

    return datetime.fromtimestamp(epochtime).strftime(fmt)


def compute_exit(entry_price, target_profit, side, entry_fee=0.04, exit_fee=0.04):
    """
    LONG: side == "BUY" => exit_price > entry_price
    SHORT: side == "SELL" => entry_price > exit_price

    to compute stop loss set `target_profit` = stoploss and
    use `side` contrary to your position
    """
    if side == "BUY":
        exit_price = (
            entry_price
            * (1 + target_profit / 100 + entry_fee / 100)
            / (1 - exit_fee / 100)
        )
    elif side == "SELL":
        exit_price = (
            entry_price
            * (1 - target_profit / 100 - entry_fee / 100)
            / (1 + exit_fee / 100)
        )
    return exit_price
