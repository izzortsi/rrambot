import numpy as np


class Strategy:
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

    def entry_signal(self, data_window):

        if np.alltrue(data_window.histogram.tail(self.entry_window) < 0):
            return True
        else:
            return False

    def exit_signal(self, trader, data_window, entry_price):

        # trader.logger.info(
        #     f"exit check, {(data_window.close.values[-1] / entry_price - 1) * 100}"
        # )

        if (
            ((data_window.close.values[-1] / entry_price - 1) * 100) * trader.leverage
            >= self.take_profit  # pelo menos `take_profit` de lucro
        ) and (np.alltrue(data_window.histogram.tail(self.exit_window) > 0)):
            return True
        else:
            return False

    def stoploss_check(self, trader, data_window, entry_price):

        value_check = (
            (data_window.close.values[-1] / entry_price - 1) * 100
        ) * trader.leverage <= self.stoploss_parameter

        # trader.logger.info(f"value check: {value_check}")

        return value_check
