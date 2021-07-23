# %%
from binance.client import Client
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)
import time
import os
import threading
from atrader import *
import strategy
import stream_processing

# from stream_processing import ProcessStream

# %%


class Manager:
    def __init__(self, api_key=None, api_secret=None):
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self.bsm = BinanceWebSocketApiManager(
            exchange="binance.com", output_default="UnicornFy"
        )
        self.stream_processer = StreamProcesser(self.bsm)
        self.traders = {}  # traders
        self.trading = []  # traders ativos

    def add_trader(self, strategy, init_val):

        name = f"{strategy.symbol}_{strategy.timeframe}_{strategy.name}"
        stream_name = f"stream_{name}"
        trader_name = f"trader_{name}"
        self.stream_processer.start_new_stream(
            f"kline_{strategy.timeframe}", strategy.symbol, stream_name=stream_name
        )

        atrader = ATrader(trader_name, self, self.stream_processer, strategy, init_val)

        self.traders[trader_name] = atrader

        return atrader

    def process_message(self, msg):
        """define how to process incoming WebSocket messages
        >essa função eu peguei de algum lugar e acho que não vou usa, senão por referência"""
        if msg["e"] != "error":
            print(msg["k"]["c"])
            self.exitprices.append(msg["k"]["c"])
            self.lastcandles.append(msg["k"])
        else:
            self.socket_error = True

    def remove_traders(self, traders, conditions=None):
        # remove um trader diretamente pelo nome ou por condiçoes (como determiná-las?)
        for name, trader in traders:
            trader.stop_trading()
            del self.traders[name]

    def get_traders(self):
        print(self.traders.keys())
        return self.traders
