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


class Trader(threading.Thread):
    def __init__(self, manager):

        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.manager = manager
        self.client = self.manager.client
        self.symbols = manager.symbols
        self.qty = self.manager.qty
        self.price_formatter = self.manager.price_formatter
        self.indicators = self.manager.indicators
        self.signals = self.manager.signals
        self.tp = self.manager.tp
        self.sl = self.manager.sl

        self.is_positioned = {symbol: None for symbol in self.symbols}
        self.position_type = {symbol: None for symbol in self.symbols}
        self.position = {symbol: None for symbol in self.symbols}
        self.entry_price = {symbol: None for symbol in self.symbols}
        self.entry_time = {symbol: None for symbol in self.symbols}
        self.exit_price = {symbol: None for symbol in self.symbols}
        self.exit_time = {symbol: None for symbol in self.symbols}
        self.exec_qty = {symbol: None for symbol in self.symbols}
        self.tp_order = {symbol: None for symbol in self.symbols}
        self.trades = {symbol: [] for symbol in self.symbols}

        self.start()

    def run(self):

        while self.manager.keep_alive:
            for symbol in self.symbols:
                # print(self.manager.signals_df[symbol])
                # print(np.any("BUY" in
                #             self.manager.signals_df[symbol].to_numpy()))
                if self.is_positioned[symbol]:
                    self.tp_order[symbol] = self.client.futures_get_order(
                        symbol=symbol.upper(), orderId=self.tp_order[symbol]["orderId"]
                    )
                    if self.tp_order[symbol]["status"] == "FILLED":
                        self.exit_price[symbol] = float(
                            self.tp_order[symbol]["avgPrice"]
                        )
                        self.exec_qty[symbol] = self.tp_order[symbol]["executedQty"]
                        self.exit_time[symbol] = to_datetime_tz(
                            self.tp_order[symbol]["updateTime"], unit="ms"
                        )
                        self.trades[symbol].append(
                            {
                                "order_id": self.tp_order[symbol]["orderId"],
                                "entry_price": self.entry_price[symbol],
                                "entry_time": self.entry_time[symbol],
                                "exit_price": self.exit_price[symbol],
                                "exit_time": self.exit_time[symbol],
                            }
                        )

                        print(
                            f"""
                        deal closed:
                        {self.trades[symbol][-1]}

                        {self.tp_order[symbol]}
                        """
                        )
                        self.is_positioned[symbol] = False
                        self.position_type[symbol] = 0
                else:
                    if np.all(substring_check("BUY", self.manager.signals_df[symbol])):

                        # self.trades[symbol].append(
                        #     f"BUY {symbol}: {self.manager.signals_df[symbol]}"
                        # )
                        self.is_positioned[symbol] = True
                        self.position_type[symbol] = 1
                        self.send_orders(symbol)
                        # print(f">>>> BUY {symbol}, {self.manager.signals_df[symbol]}")

                    elif np.all(
                        substring_check("SELL", self.manager.signals_df[symbol])
                    ):

                        self.is_positioned[symbol] = True
                        self.position_type[symbol] = -1
                        self.send_orders(symbol)

                        # self.trades[symbol].append(
                        #     f"SELL {symbol}: {self.manager.signals_df[symbol]}"
                        # )
                        # print(f">>>> SELL {symbol}, {self.manager.signals_df[symbol]}")
            time.sleep(0.2)

    def send_orders(self, symbol, protect=False):

        if self.position_type[symbol] == -1:
            side = "SELL"
            counterside = "BUY"
        elif self.position_type[symbol] == 1:
            side = "BUY"
            counterside = "SELL"

        try:
            new_position = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=self.qty[symbol],
                priceProtect=protect,
                workingType="CONTRACT_PRICE",
            )

        except BinanceAPIException as error:
            print(type(error))
            print("positioning, ", error)
        else:
            self.position[symbol] = self.client.futures_position_information(
                symbol=symbol
            )[-1]
            print(self.position[symbol])
            self.entry_price[symbol] = float(self.position[symbol]["entryPrice"])
            self.entry_time[symbol] = to_datetime_tz(
                self.position[symbol]["updateTime"], unit="ms"
            )
            # self.qty = self.position[0]["positionAmt"]
            tp_price = compute_exit(
                self.entry_price[symbol], self.tp[symbol], side=side
            )
            print("tp price", tp_price)
            tp_price = self.price_formatter(tp_price, symbol)
            entry_price = self.price_formatter(float(self.entry_price[symbol]), symbol)
            print("formatted entry price", entry_price)
            print("formatted tp price", tp_price)
            try:
                self.tp_order[symbol] = self.client.futures_create_order(
                    symbol=symbol,
                    side=counterside,
                    type="LIMIT",
                    price=tp_price,
                    workingType="CONTRACT_PRICE",
                    quantity=self.qty[symbol],
                    reduceOnly=True,
                    priceProtect=protect,
                    timeInForce="GTC",
                )
            except BinanceAPIException as error:

                print("tp order, ", error)
