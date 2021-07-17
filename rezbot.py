# %%
import grabber
import numpy as np
import pandas as pd
import argparse
from binance.client import Client
# %%

parser = argparse.ArgumentParser()
parser.add_argument("-akey", "--API_KEY", type=str)
parser.add_argument("-asec", "--API_SECRET", type=str)
parser.add_argument("-s", "--symbol", type=str, default="BTCUSDT")
parser.add_argument("-tf", "--timeframe", type=str, default="15m")
parser.add_argument("-fromdate", "--fromdate", type=str, default="2 month ago")
parser.add_argument("-todate", "--todate", type=str, default="1 month ago")
parser.add_argument("-sl", "--stoploss", type=float, default=-0.33)
parser.add_argument("-tp", "--takeprofit", type=float, default=3.5)
parser.add_argument("-ew", "--enterwindow", type=int, default=1)
parser.add_argument("-xw", "--exitwindow", type=int, default=1)

args = parser.parse_args()





class ATrader:

    def __init__(name, manager, strategy, init_val):

        self.strategy = strategy
        self.name = name
        self.init_val = init_val

        self.manager = manager
        self.is_trading = False

        self.rolling_window = Grabber...

if __name__ == __main__:
    manager = Manager(args)
    while manager.is_running:
        pass
