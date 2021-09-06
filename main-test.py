import time
from tvhandlers import ThreadedTAHandler
from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta
from manager import *
# %%

tframes

symbols = [f"{coin}usdt" for coin in coins]
# %%
m = Manager(API_KEY, API_SECRET, symbols, tframes, rate=60)
# %%
# m.stop()
#m.trader.is_alive()
# %%
# m.trader.trades
#
# m.stop()
# # %%
# m.signals_df
# np.alltrue("SELL" in m.signals_df["dotusdt"].to_numpy())
# np.alltrue("SELL" in m.signals_df["dogeusdt"].to_numpy())
# # %%
# np.all("SELL" in m.signals_df["dogeusdt"].to_numpy())
# # %%
#
# "SELL" in m.signals_df["dogeusdt"].to_numpy()
# strarray = m.signals_df["dogeusdt"].to_numpy()
# np.frompyfunc(lambda x: "SELL" in x, 1, 1)(m.signals_df["dogeusdt"].to_numpy())
# #m.stop()
# #"NEUTRAL" in m.signals_df["btcusdt"][1]
# # %%
# #m.is_monitoring
# substring_check = np.frompyfunc((lambda s, array: s in array), 2, 1)
# substring_check("SELL", strarray)
# np.all(substring_check("SELL", m.signals_df["dogeusdt"]))
