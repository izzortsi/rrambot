# %%

from src import *
from src.manager import Manager
from src.atrader import ATrader
from src.strategy import Strategy

# %%

# from src.grabber import *
# from src.strategy import *
if __name__ == "__main__":
    manager = Manager(API_KEY, API_SECRET)

    # params = {"fast": 7, "slow": 14, "signal": 5}

    # strategy1 = Strategy("macd", "ethusdt", "1m", -0.33, 3.5, 2, 2, macd_params=params)
    # strategy2 = Strategy("macd", "bnbusdt", "1m", -0.33, 3.5, 2, 2, macd_params=params)
    strategy_params = ["macd", "1m", -0.2, 1.5, 2, 1]
    strategy = Strategy("macd", "1m", -0.2, 1.5, 2, 1)
    # strategy2 = Strategy("macd", "1m", -0.2, 1.5, 2, 1)
    # strategy3 = Strategy("macd", "1m", -0.2, 1.5, 2, 1)

    # %%

    symbols = ["ethusdt", "bnbusdt", "btcusdt"]

    # %%

    t1 = manager.start_trader(strategy, symbols[0])
    t2 = manager.start_trader(strategy, symbols[1])
    t3 = manager.start_trader(strategy, symbols[2])

# %%
