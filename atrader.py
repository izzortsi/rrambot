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
    def __init__(self, name, manager, stream_processer, strategy, init_val):

        self.strategy = strategy
        self.name = name
        self.stream_name = self.name.replace("trader_", "stream_")
        self.init_val = init_val
        #self.symbol = self.strategy.symbol
        #self.timeframe = self.strategy.timeframe
        #self.state = False

        self.manager = manager
        self.stream_processer = stream_processer
        self.is_trading = False

        self.entrydates = []
        self.exitdates = []
        self.entryprices = []
        self.exitprices = []
        self.lastcandles = []
        self.log = []
        self.profits = []

    def start_trading(self, testing = True):
        """interface pra iniciar o trader, criando uma thread"""
        self.thread = threading.Thread(
            target = self.trade, name=self.name
        )
        self.thread.start()
        self.manager.trading.append(self.name)
        self.is_trading = True

    def stop_trading(self):
        """isso tem que: matar a thread da stream, matar a thread do trader e limpar tudo
        ainda falta:
        1. limpar os dados do dict
        2. """

        #mata a stream/thread
        stream = self.stream_processer.streams[self.stream_name]
        self.stream_processer.end_stream(stream)

        #tira dos traders
        self.is_trading = False
        self.manager.trading.remove(self.name)

    def trade(self):
        while self.is_trading:
            #aqui eu faço os trades. essa função não é usada diretamente
            #boa parte do que vou usar aqui tá escrita no modulo de backtest
            #o que não tá é principalmente a parte de fazer as ordens
            self.is_trading = False

##
