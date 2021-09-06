import time
from tradingview_ta import TA_Handler, Interval, Exchange, get_multiple_analysis

import tradingview_ta
import threading

import tradingview_ta
import time
import numpy as np
import os
from unicorn_binance_rest_api.unicorn_binance_rest_api_manager import (
    BinanceRestApiManager as Client,
)
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)
import pandas as pd
# %%
substring_check = np.frompyfunc((lambda s, array: s in array), 2, 1)
# %%

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

tframes = ["1m", "5m", "15m"]

coins = ["btc",
         "eth",
         "ada",
         "bnb",
         "xrp",
         "doge",
         "sol",
         "dot"]

symbols_tv = [f"binance:{coin}usdt" for coin in coins]
# %%

analysis = get_multiple_analysis(
    screener="crypto", interval="1m", symbols=symbols_tv)
# %%

analysis
for pair, A in analysis.items():
    print(A.summary)
    print(A.indicators)
# %%


class Trader(threading.Thread):

    def __init__(self, manager):

        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.manager = manager
        self.client = self.manager.client
        self.symbols = manager.symbols
        self.open_positions = []
        self.trades = []

        self.start()

    def run(self):

        while self.manager.keep_alive:
            for symbol in self.symbols:
                #print(self.manager.signals_df[symbol])
                #print(np.any("BUY" in
                #             self.manager.signals_df[symbol].to_numpy()))
                if np.all(substring_check("BUY", self.manager.signals_df[symbol])):
                    self.trades.append(
                        f"BUY {symbol}: {self.manager.signals_df[symbol]}")
                    #print(f">>>> BUY {symbol}")

                elif np.all(substring_check("SELL", self.manager.signals_df[symbol])):
                    self.trades.append(
                        f"SELL {symbol}: {self.manager.signals_df[symbol]}")
                    #print(f">>>> SELL {symbol}")
            time.sleep(0.2)


class Manager(threading.Thread):

    def __init__(self, api_key, api_secret, symbols, tframes, rate=1):

        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.client = Client(
            api_key=api_key, api_secret=api_secret, exchange="binance.com-futures"
        )

        self.symbols = symbols
        self.tframes = tframes

        self.rate = rate

        self.summaries = {symbol: {tf: None for tf in self.tframes}
                          for symbol in self.symbols}
        self.indicators = {symbol: {tf: None for tf in self.tframes}
                           for symbol in self.symbols}
        self.signals = {symbol: {tf: None for tf in self.tframes}
                        for symbol in self.symbols}

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
            time.sleep(2)

    def pcheck(self):

        print(self.signals_df)

    def stop(self):
        self.keep_alive = False


class Analyst(threading.Thread):
    def __init__(self, manager, interval, strategy=None):

        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.manager = manager
        self.symbols = self.manager.symbols
        self.symbols_tv = [
            f"binance:{symbol}" for symbol in self.symbols]
        self.strategy = strategy
        self.interval = interval
        self.rate = self.manager.rate

        self.analysises = None

        #self.keep_alive = self.manager.keep_alive

        self.is_printing = False
        self.start()

    def run(self):
        while self.manager.keep_alive:
            self.analysises = get_multiple_analysis(
                screener="crypto", interval=self.interval, symbols=self.symbols_tv)
            #print(self.interval, self.symbols_tv)
            self.process_analysises()

            time.sleep(60/self.rate)

    def stop(self):
        self.keep_alive = False

    def process_analysises(self):

        for symbol, analysis in zip(self.symbols, self.analysises.values()):

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
                "MACD_histogram": analysis.indicators["MACD.macd"] - analysis.indicators["MACD.signal"]
            }

            self.manager.indicators[symbol][self.interval] = indicators
        # recommendations.append(handler_summary["RECOMMENDATION"])
        # recommendations = np.array(recommendations)

            if (
                indicators["momentum"] >= 0 and
                indicators["MACD_histogram"] >= 0 and
                "BUY" in analysis.summary["RECOMMENDATION"]
            ):

                self.manager.signals[symbol][self.interval] = "BUY"

            elif (
                indicators["momentum"] <= 0 and
                indicators["MACD_histogram"] <= 0 and
                "SELL" in analysis.summary["RECOMMENDATION"]
            ):

                self.manager.signals[symbol][self.interval] = "SELL"

            else:

                self.manager.signals[symbol][self.interval] = "NEUTRAL"
