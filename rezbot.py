# %%

from src import *
from src.manager import Manager
from src.atrader import ATrader
from src.strategy import Strategy
import argparse

# %%
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--rate", type=int)
parser.add_argument("-sl", "--stoploss", default=-0.2, type=float)
parser.add_argument("-tp", "--takeprofit", default=1.5, type=float)
parser.add_argument("-L", "--leverage", default=1, type=int)
args = parser.parse_args()

rate = args.rate
tp = args.takeprofit
sl = args.stoploss
leverage = args.leverage
# %%

# from src.grabber import *
# from src.strategy import *
if __name__ == "__main__":
    manager = Manager(API_KEY, API_SECRET, rate=rate)

    # params = {"fast": 7, "slow": 14, "signal": 5}

    # strategy1 = Strategy("macd", "ethusdt", "1m", -0.33, 3.5, 2, 2, macd_params=params)
    # strategy2 = Strategy("macd", "bnbusdt", "1m", -0.33, 3.5, 2, 2, macd_params=params)
    # strategy_params = ["macd", "1m", -0.2, 1.5, 2, 1]
    strategy_params = ["macd", "1m", sl, tp, 2, 1]
    strategy = Strategy(*strategy_params)
    # strategy2 = Strategy("macd", "1m", -0.2, 1.5, 2, 1)
    # strategy3 = Strategy("macd", "1m", -0.2, 1.5, 2, 1)

    # %%

    symbols = ["ethusdt", "bnbusdt", "btcusdt"]

    # %%

    t1 = manager.start_trader(strategy, symbols[0], leverage=leverage)
    t2 = manager.start_trader(strategy, symbols[1], leverage=leverage)
    t3 = manager.start_trader(strategy, symbols[2], leverage=leverage)

# %%
