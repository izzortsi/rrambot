import numpy as np
import time


class MacdStrategy:
    def __init__(
        self,
        name,
        timeframe,
        stoploss_parameter,
        take_profit,
        entry_window,
        exit_window,
        macd_params={"fast": 12, "slow": 26, "signal": 9},
    ):
        self.name = name
        self.timeframe = timeframe
        self.stoploss_parameter = stoploss_parameter
        self.take_profit = take_profit
        self.entry_window = entry_window
        self.exit_window = exit_window
        self.macd_params = macd_params

    def entry_signal(self, trader):

        if np.alltrue(trader.data_window.histogram.tail(self.entry_window) < 0):
            return True
        else:
            return False

    def exit_signal(self, trader):

        condition1 = trader.current_percentual_profit >= self.take_profit

        condition2 = np.alltrue(
            trader.data_window.histogram.tail(self.exit_window) > 0)
        check = condition1 and condition2

        return check

    def stoploss_check(self, trader):

        check = trader.current_percentual_profit <= self.stoploss_parameter

        return check


class TAStrategy:
    def __init__(
        self,
        name,
        timeframe,
        stoploss_parameter,
        take_profit,
        entry_window,
        exit_window,
        macd_params={"fast": 12, "slow": 26, "signal": 9},
    ):
        self.name = name
        self.timeframe = timeframe
        self.stoploss_parameter = stoploss_parameter
        self.take_profit = take_profit
        self.entry_window = entry_window
        self.exit_window = exit_window
        self.macd_params = macd_params

    def entry_signal(self, trader):

        if (np.alltrue(trader.data_window.histogram.tail(self.entry_window) < 0)
                and trader.ta_signal):
            return True
        else:
            return False

    def exit_signal(self, trader):

        condition1 = trader.current_percentual_profit >= self.take_profit

        condition2 = np.alltrue(
            trader.data_window.histogram.tail(self.exit_window) > 0)
        check = condition1 and condition2

        return check

    def stoploss_check(self, trader):

        check = trader.current_percentual_profit <= self.stoploss_parameter

        return check
