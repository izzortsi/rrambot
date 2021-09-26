import datetime
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
from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta

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


# def round_step_size(
#     quantity: Union[float, Decimal], step_size: Union[float, Decimal]
# ) -> float:
#     """Rounds a given quantity to a specific step size
#
#     :param quantity: required
#     :param step_size: required
#
#     :return: decimal
#     """
#     precision: int = int(round(-math.log(step_size, 10), 0))
#     return float(round(quantity, precision))


substring_check = np.frompyfunc((lambda s, array: s in array), 2, 1)
