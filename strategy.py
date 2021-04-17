##
import pandas as pd

##


##
class Strategy:
    def __init__(self, data, stoploss_parameter, take_profit, entry_conditions = None, exit_conditions = None, stoploss_conditions = None):
        
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
