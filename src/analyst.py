# import time
# from tradingview_ta import TA_Handler, Interval, Exchange, get_multiple_analysis
#
# import tradingview_ta
# import threading
# import tradingview_ta
# import time
# import numpy as np
# import os
# from unicorn_binance_rest_api.unicorn_binance_rest_api_manager import (
#     BinanceRestApiManager as Client,
# )
# from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
#     BinanceWebSocketApiManager,
# )
# from unicorn_binance_rest_api.unicorn_binance_rest_api_exceptions import *
# from imports_auxs_consts import *
# import pandas as pd
# from symbols_formats import FORMATS
from src.imports import *

# %%
# substring_check = np.frompyfunc((lambda s, array: s in array), 2, 1)
#
#
# def side_from_int(self):
#     if self.position_type == -1:
#         return "SELL", "BUY"
#     elif self.position_type == 1:
#         return "BUY", "SELL"
#
#
# # %%
#
# API_KEY = os.environ.get("API_KEY")
# API_SECRET = os.environ.get("API_SECRET")
#
# tframes = ["5m", "15m", "1h"]
#
# coins = ["eth", "ada", "bnb", "xrp", "doge", "dot", "xlm", "iota", "dash"]
#
# symbols_tv = [f"binance:{coin}usdt" for coin in coins]

# %%


class Analyst(threading.Thread):
    def __init__(self, manager, interval, strategy=None):

        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.manager = manager
        self.symbols = self.manager.symbols
        self.symbols_tv = [f"binance:{symbol}" for symbol in self.symbols]
        self.strategy = strategy
        self.interval = interval
        self.rate = self.manager.rate

        self.analysises = None

        # self.keep_alive = self.manager.keep_alive

        self.is_printing = False
        self.start()

    def run(self):
        while self.manager.keep_alive:
            self.analysises = get_multiple_analysis(
                screener="crypto", interval=self.interval, symbols=self.symbols_tv
            )
            # print(self.interval, self.symbols_tv)
            self.process_analysises()

            time.sleep(60 / self.rate)

    def stop(self):
        self.keep_alive = False

    def process_analysises(self):

        for symbol, analysis in self.analysises.items():
            symbol = symbol.split(":")[-1]
            # print(symbol)
            self.manager.summaries[symbol][self.interval] = analysis.summary
            # self.indicators[symbol] = {
            #     indicator: analysis.indicators[indicator]
            #     for indicator in self.strategy.indicators}

            indicators = {
                "open": analysis.indicators["open"],
                # "high": analysis.indicators["high"],
                # "low": analysis.indicators["low"],
                "close": analysis.indicators["close"],
                "volume": analysis.indicators["volume"],
                "momentum": analysis.indicators["Mom"],
                "RSI": analysis.indicators["RSI"],
                "MACD_histogram": analysis.indicators["MACD.macd"]
                - analysis.indicators["MACD.signal"],
            }

            self.manager.indicators[symbol][self.interval] = indicators
            # recommendations.append(handler_summary["RECOMMENDATION"])
            # recommendations = np.array(recommendations)

            if (
                # indicators["RSI"] <= 50
                "BUY"
                in analysis.summary["RECOMMENDATION"]
                # indicators["momentum"] >= 0
                # and indicators["MACD_histogram"] >= 0
                # and "BUY" in analysis.summary["RECOMMENDATION"]
            ):

                self.manager.signals[symbol][self.interval] = "BUY"

            elif (
                # indicators["RSI"] >= 50
                "SELL"
                in analysis.summary["RECOMMENDATION"]
                # indicators["momentum"] <= 0
                # and indicators["MACD_histogram"] <= 0
                # and "SELL" in analysis.summary["RECOMMENDATION"]
            ):

                self.manager.signals[symbol][self.interval] = "SELL"

            else:

                self.manager.signals[symbol][self.interval] = "NEUTRAL"


# %%
