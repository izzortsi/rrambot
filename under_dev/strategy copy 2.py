##
import pandas as pd
from dataclasses import dataclass
##


##
class Strategy:
    def __init__(self, data, entry_conditions, exit_conditions, stoploss_conditions, stoploss_parameter, take_profit):
        
        self.df = data
        self.indicators = self.df.loc[:, self.df.columns != "close"]
        self.closes = self.df["close"]
        self.datasize = len(self.closes)
        
        self.entry_conditions = entry_conditions
        self.exit_conditions = exit_conditions
        self.stoploss_conditions = stoploss_conditions
        self.stoploss_parameter = stoploss_parameter
        self.take_profit = take_profit

##

class Foo(object):
    CONFIG = {
        "p1": 10,
        "p2": 20
    }

##

Foo()

##
Foo.CONFIG
##
