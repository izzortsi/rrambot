# %%
from binance.client import Client
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)
import time
import os
import threading
from atrader import *
from strategy import *

# from stream_processing import ProcessStream

# %%


class Manager:
    def __init__(self, api_key=None, api_secret=None):
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self.bsm = BinanceWebSocketApiManager(
            exchange="binance.com", output_default="UnicornFy"
        )
        self.traders = {}
        self.trading = []

    def add_trader(self, strategy, init_val):

        name = f"{strategy.symbol}_{strategy.timeframe}_{strategy.name}"

        trader_id = self.bsm.create_stream(
            f"kline_{strategy.timeframe}",
            strategy.symbol,
            stream_label=name,
            stream_buffer_name=name,
            output="UnicornFy",
        )

        atrader = ATrader(name, self, trader_id, strategy, init_val)

        self.traders[name] = atrader

        return atrader

    def process_message(self, msg):
        """ define how to process incoming WebSocket messages """
        if msg["e"] != "error":
            print(msg["k"]["c"])
            self.exitprices.append(msg["k"]["c"])
            self.lastcandles.append(msg["k"])
        else:
            self.socket_error = True

    def remove_trader(self, name=None, conditions=None):
        # remove um trader diretamente pelo nome ou por condiçoes (como determiná-las?)
        raise NotImplementedError

    def get_traders(self):
        print(self.traders.keys())
        return self.traders
