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
#
# # %%
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
from src.imports import *
from src.analyst import Analyst
from src.trader import Trader
from unicorn_binance_rest_api.unicorn_binance_rest_api_manager import (
    BinanceRestApiManager as Client,
)

# %%


class Manager(threading.Thread):
    def __init__(
        self,
        api_key,
        api_secret,
        symbols,
        tframes,
        rate=1,
        qty=2,
        leverage=3,
        tp=0.03,
        sl=-0.02,
    ):

        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.client = Client(
            api_key=api_key, api_secret=api_secret, exchange="binance.com-futures"
        )

        self.symbols = symbols
        self.tframes = tframes

        self.rate = rate

        self.summaries = {
            symbol: {tf: None for tf in self.tframes} for symbol in self.symbols
        }
        self.indicators = {
            symbol: {tf: None for tf in self.tframes} for symbol in self.symbols
        }
        self.signals = {
            symbol: {tf: None for tf in self.tframes} for symbol in self.symbols
        }
        self.min_multiplier = qty
        self.qty = {symbol: None for symbol in self.symbols}
        self.tp = {symbol: tp for symbol in self.symbols}
        self.sl = {symbol: sl for symbol in self.symbols}
        self.leverage = {symbol: leverage for symbol in self.symbols}
        # self.price_formatter = {symbol: None for symbol in self.symbols}
        # self.price_formatter = lambda self, x, symbol: f"{x:.{price_precision}f}"
        self.format = {symbol: None for symbol in self.symbols}
        self.set_formats()
        self.set_leverages()

        self.signals_df = None
        self.keep_alive = True
        self.analysts = {}
        self.trader = None
        self.is_monitoring = False
        self.start()

    def make_analysts(self):

        for tf in self.tframes:
            self.analysts[tf] = Analyst(self, tf, self.rate)

    def run(self):
        self.make_analysts()
        time.sleep(5)
        self.signals_df = pd.DataFrame.from_dict(self.signals)
        time.sleep(2)
        self.trader = Trader(self)
        while self.keep_alive:
            self.signals_df = pd.DataFrame.from_dict(self.signals, dtype=str)
            if self.is_monitoring:
                self.pcheck()
            time.sleep(0.5)

    def pcheck(self):

        print(self.signals_df)

    def stop(self, q=0):
        self.keep_alive = False
        if q == 0:
            os.sys.exit()

    def price_formatter(self, x, symbol):
        precision = self.format[symbol]["tickSize"]
        return f"{x:.{precision}f}"

    def set_formats(self):
        for symbol in self.symbols:
            if symbol.upper() in FORMATS.keys():
                format = FORMATS[symbol.upper()]
                qty_precision = int(format["quantityPrecision"])
                price_precision = int(format["pricePrecision"])
                tick_size = int(format["tickSize"])
                format["quantityPrecision"] = qty_precision
                format["pricePrecision"] = price_precision
                format["tickSize"] = tick_size
                self.format[symbol] = format
                # print(qty_precision)
                # print(price_precision)
                notional = 5
                min_qty = 1 / 10 ** qty_precision

                ticker = self.client.get_symbol_ticker(symbol=symbol.upper())
                price = float(ticker["price"])
                multiplier = self.min_multiplier * np.ceil(notional / (price * min_qty))
                # f"{float(value):.{decimal_count}f}"

                self.qty[symbol] = f"{float(multiplier*min_qty):.{qty_precision}f}"
                # self.price_formatter[symbol] = lambda x: f"{x:.{price_precision}f}"
                print(
                    f"""
                {symbol}
                {min_qty}
                {qty_precision}, {price_precision}, {tick_size}
                {self.qty[symbol]}
                {self.price_formatter(price, symbol)}"""
                )

    def set_leverages(self):
        for symbol in self.symbols:
            self.client.futures_change_leverage(
                symbol=symbol, leverage=self.leverage[symbol]
            )
