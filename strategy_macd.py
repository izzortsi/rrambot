##
import pandas as pd
from strategy import Strategy
from grabber import *
import numpy as np
##
class MacdStrategy(Strategy):
    def __init__(self, n1, n2, *args, **kwargs):
        self.n1 = n1
        self.n2 = n2
        supargs = list(args)
        supkwargs = dict(kwargs)
        super().__init__(*supargs, **supkwargs)
        self.histogram = self.indicators["histogram"]

    def
        client = Client()
        grab = GrabberMACD(client)
        grab.get_data()
        self.df = grab.compute_indicators()

    def E(self, i):

        if np.alltrue(self.histogram.iloc[:i].tail(self.n1) < 0):
            return True
        else:
            return False

    def X(self, i, buy_price):

        if (
            ((self.prices.iloc[i]/buy_price - 1)*100 >= self.take_profit) and #pelo menos `take_profit` de lucro
            (np.alltrue(self.histogram.iloc[:i].tail(self.n2) > 0))
            ):
            return True
        else:
            return False

    def stoploss_check(self, i, buy_price):
        return ((self.prices.iloc[i]/buy_price - 1)*100 <= self.stoploss_parameter)



##
from binance.client import Client
##
client = Client()
grab = GrabberMACD(client)
grab.get_data()
df = grab.compute_indicators()
##
df
##
macd_strat = MacdStrategy(1, 2, df, 2.4, 0)
##
macd_strat.E(1)
##
macd_strat.histogram
##
