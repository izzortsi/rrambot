# %%
from manager import *
from atrader import *
from stream_processing import *
from strategy import *
from grabber import *

# %%

manager = Manager()
# %%
manager.bsm.pop_stream_data_from_stream_buffer

# %%
# parameters

symbol = "ADABTC"
tframe = "15m"
limit = 100
stoploss_parameter = -0.27
take_profit = 2.5
n1 = 9
n2 = 3
# %%
grabber = GrabberMACD(manager.client)
strat = MacdStrategy(
    9,
    3,
    grabber,
    symbol,
    tframe,
    stoploss_parameter,
    take_profit,
    limit=100,
)
# %%

# %%
trader1 = manager.add_trader(strat, 100)
# %%
trader1.trade()
# %%
manager.trading

# %%
trader1.stream_processer.data
# %%
trader1.thread
trader1.name
# %%
trader1.strategy
trader1.stream_processer.keep_running = False

trader1.stream_processer.data
# %%
