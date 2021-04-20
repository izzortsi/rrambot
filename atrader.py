# %%
import os
import time
import threading

# from strategy_macd import MacdStrategy
from strategy import *
from stream_processing import StreamProcesser
from grabber import *

# %%


class ATrader:
    def __init__(self, name, manager, stream_id, strategy, init_val):

        self.strategy = strategy
        self.name = name
        self.init_val = init_val
        self.symbol = strategy.symbol
        self.timeframe = strategy.timeframe
        self.state = False

        self.manager = manager
        self.stream_id = stream_id
        self.socket_error = False

        self.entrydates = []
        self.exitdates = []
        self.entryprices = []
        self.exitprices = []
        self.lastcandles = []
        self.log = []
        self.profits = []

    def trade(self):
        self.stream_processer = StreamProcesser(self.manager.bsm, self.name)

        self.thread = threading.Thread(
            target=self.stream_processer.process_stream, name=self.name
        )
        self.thread.start()
        self.manager.trading.append(self.name)

    def stop_trading(self):
        self.stream_processer.keep_running = False
        self.manager.trading.remove(self.name)


##
