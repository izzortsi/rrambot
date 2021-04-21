# %%
from manager import *
from atrader import *
from stream_processing import *
from strategy import *
from grabber import *
from operator import itemgetter

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
symbol = "ETHUSDT"
tframe = "15m"
limit = 100
stoploss_parameter = -0.27
take_profit = 2.5
n1 = 9
n2 = 3

# %%
strat2 = MacdStrategy(
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
trader2 = manager.add_trader(strat2, 100)
# %%
trader2.trade()
# %%

trader1.thread == trader2.thread
# %%
trader1.stop_trading()
trader2.stop_trading()

# %%
trader1.stream_processer.data
trader2.stream_processer.data

traders = manager.get_traders()
manager.remove_traders(traders)
# %%

# %%
trader1.stream_processer.data

# %%

# %%
