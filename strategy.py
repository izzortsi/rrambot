# %%
import pandas as pd
import numpy as np
from grabber import *

# %%


class Strategy:
    def __init__(
        self,
        name,
        grabber,
        symbol,
        timeframe,
        stoploss_parameter,
        take_profit,
        limit=None,
        entry_conditions=None,
        exit_conditions=None,
        stoploss_conditions=None,
    ):
        self.name = name
        self.symbol = symbol
        self.timeframe = timeframe
        self.grabber = grabber
        self.grabber.get_data(symbol=symbol, tframe=timeframe, limit=limit)
        self.df = self.grabber.compute_indicators()
        self.indicators = self.df.loc[:, self.df.columns != "close"]
        self.closes = self.df["close"]
        self.datasize = len(self.closes)

        self.entry_conditions = entry_conditions
        self.exit_conditions = exit_conditions
        self.stoploss_conditions = stoploss_conditions

        self.stoploss_parameter = stoploss_parameter
        self.take_profit = take_profit


class MacdStrategy(Strategy):
    def __init__(self, n1, n2, *args, **kwargs):
        self.n1 = n1
        self.n2 = n2
        # supargs = list(args)
        # supkwargs = dict(kwargs)
        print(kwargs)
        super().__init__("brainded_macd", *args, **kwargs)
        self.histogram = self.indicators["histogram"]

    def E(self, i):

        if np.alltrue(self.histogram.iloc[:i].tail(self.n1) < 0):
            return True
        else:
            return False

    def X(self, i, buy_price):

        if (
            (self.closes.iloc[i] / buy_price - 1) * 100 >= self.take_profit
        ) and (  # pelo menos `take_profit` de lucro
            np.alltrue(self.histogram.iloc[:i].tail(self.n2) > 0)
        ):
            return True
        else:
            return False

    def stoploss_check(self, i, buy_price):
        return (self.closes.iloc[i] / buy_price - 1) * 100 <= self.stoploss_parameter


##
