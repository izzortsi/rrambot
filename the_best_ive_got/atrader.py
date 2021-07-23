# %%
import os
import time
import threading

# from strategy_macd import MacdStrategy
from strategy import *
from stream_processing import StreamProcesser
from grabber import DataGrabber

# %%


class ATrader:
    def __init__(self, manager, strategy, initial_value):

        self.manager = manager
        self.client = manager.client
        self.bswm = manager.bswm

        self.symbol = strategy.symbol
        self.timeframe = strategy.timeframe
        self.initial_value = initial_value
        self.stoploss_parameter = strategy.stoploss_parameter
        self.take_profit = strategy.take_profit
        self.entry_window = strategy.entry_window
        self.exit_window = strategy.exit_window
        self.macd_params = strategy.macd_params

        self.grabber = DataGrabber(self.client)
        self.data_window = self._get_initial_data_window()
        # self.last_mark_price = self.grabber.get_data(symbol=self.symbol, tframe = self.timeframe, limit = 1)
        # self.data_window.append(self.last_)
        # self.last_histogram = self.data_window.tail(1).histogram
        self.init_time = time.time()

        self.is_positioned = False
        self.entry_price = None

    def _start_futures_stream(self):
        stream_id = self.bswm.create_stream(
            ["!markPrice"], "arr@1s", stream_label="!markPrice@arr@1s"
        )
        # stream = f"{self.symbol}@markPrice@1s"
        self.stream_name = stream_id
        return self.stream_name

    def handle_stream_message(self, msg):

        tf_as_seconds = interval_to_milliseconds(self.strategy.timeframe) * 0.001

        now = time.time()
        new_row = self.grabber.trim_data(msg["data"]["k"]).compute_indicators()

        if int(now - self.init_time) >= tf_as_seconds:

            self.data_window = self.data_window.drop(self.data_window.iloc[[0]].index)

            self.data_window = self.data_window.append(new_row)

        else:
            self.data_window.iloc[[-1]] = new_row

        self.act_on_signal(self)

    def signal_from_strategy(self):
        pass

    def act_on_signal(self):
        """
        aqui eu tenho que
        1) mudar o sinal de entrada pra incluir as duas direçoes
        2) ver se realmente preciso dessas funçoes ou se dá pra deixar
        toda a operação dentro dessa mesma
        3) de qualquer forma, essa é a função que faz os trades, efetivamente
        """
        if self.is_positioned:
            if strategy.stoploss_check(self.data_window, self.entry_price):
                return stop_loss()
            elif strategy.exit_signal(self.data_window, self.entry_price):
                return take_profit()
        else:
            if strategy.entry_signal(self.data_window):
                return take_position()

    def _get_initial_data_window(self):
        klines = self.grabber.get_data(
            symbol=self.symbol,
            tframe=self.timeframe,
            limit=2 * self.macd_params["window_slow"],
        )
        last_kline_row = self.grabber.get_data(
            symbol=self.symbol, tframe=self.timeframe, limit=1
        )
        klines = klines.append(last_kline_row, ignore_index=True)
        c = klines.close
        date = klines.date
        macd = ta.macd(c)
        df = pd.concat([date, c, macd], axis=1)
        return df


class ATrader:
    def __init__(self, name, manager, stream_processer, strategy, init_val):

        self.strategy = strategy
        self.name = name
        self.stream_name = self.name.replace("trader_", "stream_")
        self.init_val = init_val
        # self.symbol = self.strategy.symbol
        # self.timeframe = self.strategy.timeframe
        # self.state = False

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

    def start_trading(self, testing=True):
        """interface pra iniciar o trader, criando uma thread"""
        self.thread = threading.Thread(target=self.trade, name=self.name)
        self.thread.start()
        self.manager.trading.append(self.name)
        self.is_trading = True

    def stop_trading(self):
        """isso tem que: matar a thread da stream, matar a thread do trader e limpar tudo
        ainda falta:
        1. limpar os dados do dict
        2."""

        # mata a stream/thread
        stream = self.stream_processer.streams[self.stream_name]
        self.stream_processer.end_stream(stream)

        # tira dos traders
        self.is_trading = False
        self.manager.trading.remove(self.name)

    def trade(self):
        while self.is_trading:
            # aqui eu faço os trades. essa função não é usada diretamente
            # boa parte do que vou usar aqui tá escrita no modulo de backtest
            # o que não tá é principalmente a parte de fazer as ordens
            self.is_trading = False


##
