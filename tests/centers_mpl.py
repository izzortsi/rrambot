# %%


import pandas as pd
import pandas_ta as ta
from binance.client import Client
import matplotlib.pyplot as plt

# %%


# Load data

client = Client()
klines = client.get_historical_klines("ETHUSDT", "1h", "3 day ago")

# %%


def trim_data(rdata):
    df = pd.DataFrame(data=rdata)
    DOHLCV = df.iloc[:, [0, 1, 2, 3, 4, 5]]
    DOHLCV[0] = pd.to_datetime(DOHLCV[0], unit="ms")
    DOHLCV.columns = ["date", "open", "high", "low", "close", "volume"]
    OHLCV = DOHLCV.iloc[:, [1, 2, 3, 4, 5]]
    OHLCV.set_index(pd.DatetimeIndex(DOHLCV["date"]), inplace=True)
    OHLCV = OHLCV.astype("float64")
    return OHLCV


def plots(c, cs, cm, ci, mom, macd):

    ax2 = plt.subplot(311)
    ax2.plot(c, "k-", linewidth=0.9, label="closes")
    ax2.plot(cs, "g--", linewidth=0.9, label="superior center")
    ax2.plot(cm, "b--", linewidth=0.9, label="medium center")
    ax2.plot(ci, "r--", linewidth=0.9, label="inferior center")
    ax2.grid(True)
    ax2.xaxis.grid(True, which="both")
    ax2.xaxis.grid(which="minor", linestyle="--", alpha=0.5)

    ax3 = plt.subplot(312, sharex=ax2)
    ax3.plot(mom, "k-", linewidth=0.9, label="momentum")
    #    ax3.plot(cs,"g--",linewidth=0.9, label="superior center")
    #    ax3.plot(cm,"b--",linewidth=0.9, label="medium center")
    #    ax3.plot(ci, "r--", linewidth=0.9, label="inferior center")
    ax3.grid(True)
    ax3.xaxis.grid(True, which="both")
    ax3.xaxis.grid(which="minor", linestyle="--", alpha=0.5)

    ax4 = plt.subplot(313, sharex=ax2)
    ax4.plot(macd["MACDh_12_26_9"], "k-", linewidth=0.9, label="macd histogram")
    #    ax4.plot(cs,"g--",linewidth=0.9, label="superior center")
    #    ax4.plot(cm,"b--",linewidth=0.9, label="medium center")
    #    ax4.plot(ci, "r--", linewidth=0.9, label="inferior center")
    ax4.grid(True)
    ax4.xaxis.grid(True, which="both")
    ax4.xaxis.grid(which="minor", linestyle="--", alpha=0.5)


# %%


ohlcv = trim_data(klines)
ohlc = ohlcv.drop(columns=["volume"])
hlc = ohlc.drop(columns=["open"])

c = ohlcv.pop("close")
h = ohlcv.pop("high")
l = ohlcv.pop("low")
v = ohlcv.pop("volume")

# %%


# vwap = ta.vwap(ohlcv["high"], ohlcv["low"], ohlcv["close"], ohlcv["volume"])
# hlcvwap = pd.concat([hlc, vwap], axis=1)

# %%


cs = ta.vwma(h, v, length=3)
cm = ta.vwma(c, v, length=3)
ci = ta.vwma(l, v, length=3)

# %%


# roc = ta.roc(c, length=5)
rsi = ta.rsi(c, length=7)
rsi
macd = ta.macd(c)
macd
# %%


df = pd.concat([cs, ci, c, cm], axis=1)

# %%


macd
# %%


plt.ion()
# df.plot(style=["g--", "r--", "k-", "b-."])
# %%


plots(c, cs, cm, ci, rsi, macd)
# %%


# %%
