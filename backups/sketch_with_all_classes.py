# %%
import os
import time
import threading
import numpy as np
import pandas as pd
from grabber import DataGrabber

from unicorn_binance_rest_api.unicorn_binance_rest_api_manager import (
    BinanceRestApiManager as Client,
)

from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)
from unicorn_binance_rest_api.unicorn_binance_rest_api_helpers import (
    interval_to_milliseconds,
)

# %%

api_key = ""
api_secret = ""


class Manager:
    def __init__(self, api_key, api_secret):
        self.traders = {}
        self.client = Client(api_key=api_key, api_secret=api_secret, tld="com")
        self.bwsm = BinanceWebSocketApiManager(exchange="binance.com-futures")

    def start_trader(self, strategy):
        trader = ATrader(self, strategy)
        self.traders[trader] = trader


# %%

# %%


class ATrader:
    def __init__(self, manager, strategy, initial_value):
        self.data = []
        self.manager = manager
        self.client = manager.client
        self.bwsm = manager.bwsm
        self.strategy = strategy

        self.symbol = strategy.symbol
        self.timeframe = strategy.timeframe
        self.is_trading = True
        self.init_time = time.time()

        self.stream_id = self.bwsm.create_stream(
            [self.strategy.symbol],
            f"@kline_{self.strategy.timeframe}",
            stream_label=self.strategy.symbol + f"@kline_{self.strategy.timeframe}",
        )
        # stream = f"{self.symbol}@markPrice@1s"

        self.worker_thread = threading.Thread(target=self._trade, args=())
        self.worker_thread.start()

    def _start_working_trader(self):
        pass

    def _trade(self):

        time.sleep(2)
        tf_as_seconds = interval_to_milliseconds(self.strategy.timeframe) * 0.001

        now = time.time()

        data_from_stream_buffer = self.bwsm.pop_stream_data_from_stream_buffer(
            self.stream_id
        )
        # new_row = self.grabber.trim_data(msg["data"]["k"]).compute_indicators()
        while self.is_trading:
            time.sleep(5)
            if int(now - self.init_time) >= 10:  # tf_as_seconds:
                self.data.append(data_from_stream_buffer)
                self.init_time = time.time()
        #     self.data_window = self.data_window.drop(
        #         self.data_window.iloc[[0]].index)
        #
        #     self.data_window = self.data_window.append(new_row)
        #
        # else:
        #     self.data_window.iloc[[-1]] = new_row

        def stop(self):
            self.is_trading = False


# %%


class Strategy:
    def __init__(
        self,
        symbol,
        timeframe,
        stoploss_parameter,
        take_profit,
        entry_window,
        exit_window,
        macd_params={"window_slow": 26, "window_fast": 12, "window_sign": 9},
    ):
        self.symbol = symbol
        self.timeframe = timeframe
        self.stoploss_parameter = stoploss_parameter
        self.take_profit = take_profit
        self.entry_window = entry_window
        self.exit_window = exit_window
        self.macd_params = macd_params

    def entry_signal(self, data_window):

        if np.alltrue(data_window.histogram.tail(self.entry_window) < 0):
            return True
        else:
            return False

    def exit_signal(self, data_window, entry_price):

        if (
            (self.data_window.closes / entry_price - 1) * 100
            >= self.take_profit  # pelo menos `take_profit` de lucro
        ) and (np.alltrue(data_window.histogram.tail(self.exit_window) > 0)):
            return True
        else:
            return False

    def stoploss_check(self, data_window, entry_price):

        return (data_window.closes / entry_price - 1) * 100 <= self.stoploss_parameter


# %%
manager = Manager(api_key, api_secret)
strategy = Strategy("BNBUSDT", "15m", -0.33, 3.5, 2, 2)
# %%
atrader = ATrader(manager, strategy, 1)
# %%

atrader.worker_thread.isDaemon()
atrader.data

manager.bwsm.get_active_stream_list()
atrader.stop()
