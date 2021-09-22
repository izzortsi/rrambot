from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.stats
import pandas as pd
import pandas_ta as ta

# escrever as funcoes pra calcular os indicadores,
# preocupar-se com a interface... nao precisa fazer quase nada, usando o pandas_ta
##
import pandas as pd
import pandas_ta as ta

##
class HistoricalGrabber:
    def __init__(self, client):
        self.client = client

    def get_data(
        self, symbol="BTCUSDT", tframe="1h", fromdate="3 day ago", todate=None
    ):

        self.klines = self.client.get_historical_klines(
            symbol, tframe, fromdate, end_str=todate
        )
        self.trim_data()
        # replaced_fromdate = fromdate.replace(" ", "-")

    def trim_data(self):

        df = pd.DataFrame(data=self.klines)
        DOHLCV = df.iloc[:, [0, 1, 2, 3, 4, 5]]
        DOHLCV[0] = pd.to_datetime(DOHLCV[0], unit="ms")
        DOHLCV.columns = ["date", "open", "high", "low", "close", "volume"]
        OHLCV = DOHLCV.iloc[:, [1, 2, 3, 4, 5]]
        OHLCV.set_index(pd.DatetimeIndex(DOHLCV["date"]), inplace=True)
        OHLCV = OHLCV.astype("float64")
        self.ohlcv = OHLCV

    def compute_indicators(self, indicators=[]):

        c = self.ohlcv["close"]
        h = self.ohlcv["high"]
        l = self.ohlcv["low"]
        v = self.ohlcv["volume"]

        cs = ta.vwma(h, v, length=3)
        cs.rename("csup", inplace=True)

        cm = ta.vwma(c, v, length=3)
        cm.rename("cmed", inplace=True)

        ci = ta.vwma(l, v, length=3)
        ci.rename("cinf", inplace=True)

        macd = ta.macd(c)

        df = pd.concat([cs, ci, c, cm, v], axis=1)

        return df


class HistoricalMACDGrabber(HistoricalGrabber):
    def compute_indicators(self, indicators=[]):

        c = self.ohlcv["close"]
        h = self.ohlcv["high"]
        l = self.ohlcv["low"]
        v = self.ohlcv["volume"]

        macd = ta.macd(c)

        df = pd.concat([c, macd], axis=1)

        return df


##
def get_data(symbol, tframe, fromdate):
    klines = client.get_historical_klines(symbol, tframe, fromdate)
    replaced_fromdate = fromdate.replace(" ", "-")
    return trim_data(klines)


def trim_data(rdata):
    df = pd.DataFrame(data=rdata)
    DOHLCV = df.iloc[:, [0, 1, 2, 3, 4, 5]]
    DOHLCV[0] = pd.to_datetime(DOHLCV[0], unit="ms")
    DOHLCV.columns = ["date", "open", "high", "low", "close", "volume"]
    DOHLCV.ta.adjusted = "adj_close"
    OHLCV = DOHLCV.iloc[:, [1, 2, 3, 4, 5]]
    OHLCV.set_index(pd.DatetimeIndex(DOHLCV["date"]), inplace=True)
    OHLCV = OHLCV.astype("float64")
    return OHLCV


ta.vwma()

Indicators = ta.Strategy(
    name="EMAs, BBs, and MACD",
    description="Non Multiprocessing Strategy by rename Columns?",
    ta=[
        {"kind": "ema", "length": 8},
        {"kind": "ema", "length": 21},
        {"kind": "bbands", "length": 20, "col_names": ("BBL", "BBM", "BBU")},
        {
            "kind": "macd",
            "fast": 8,
            "slow": 21,
            "col_names": ("MACD", "MACD_H", "MACD_S"),
        },
    ],
)
# Run it
df.ta.strategy(NonMPStrategy)

# %%
output_file(f"{symbol}_{tframe}_{replaced_fromdate}.html")


# %%
ohlcv = get_data(symbol, tframe, fromdate)
c = ohlcv["close"]
h = ohlcv["high"]
l = ohlcv["low"]
v = ohlcv["volume"]
# %%
ta.mom(v, length=4)
# %%
# ohlcv.ta.adjusted = "adj_close"

# df.ta.adjusted = None
# ohlc = ohlcv.drop(columns=["volume"])
# hlc = ohlc.drop(columns=["open"])

# %%


cs = ta.vwma(h, v, length=N)
cs.rename("csup", inplace=True)

cm = ta.vwma(c, v, length=N)
cm.rename("cmed", inplace=True)

ci = ta.vwma(l, v, length=3)
ci.rename("cinf", inplace=True)
# %%


# roc = ta.roc(c, length=5)
rsi = ta.rsi(c, length=7)
# %%
# rsi_mean = rsi.mean()
# rsi_std = rsi.std()
# rsi = (rsi - rsi_mean)/rsi_std
# %%


# %%
macd = ta.macd(c)
macd_h = macd["MACDh_12_26_9"]
# %%
macd_mean = macd.mean()
macd_std = macd.std()

macd = (macd - macd_mean) / macd_std
macd
# %%
macd_h = macd["MACDh_12_26_9"]
# hstd = macd_h.std()
# hmean = macd_h.mean()
# nmacd_h = (macd_h - hmean) / hstd
# %%
D1h = macd_h.shift(1) - macd_h
# D1h = (D1h - D1h.mean()) / D1h.std()
D1h = D1h.rename("D1h")
D2h = D1h.shift(1) - D1h
# D2h = (D2h - D2h.mean()) / D2h.std()
D2h = D2h.rename("D2h")

# %%
df = pd.concat([cs, ci, c, cm, v, macd, rsi, D1h, D2h], axis=1)

# %%
class DataGrabber:
    def __init__(self, client):
        self.client = client

    def get_data(symbol, tframe, fromdate):
        klines = client.get_historical_klines(symbol, tframe, fromdate)
        replaced_fromdate = fromdate.replace(" ", "-")
        return trim_data(klines)

    def trim_data(rdata):
        df = pd.DataFrame(data=rdata)
        DOHLCV = df.iloc[:, [0, 1, 2, 3, 4, 5]]
        DOHLCV[0] = pd.to_datetime(DOHLCV[0], unit="ms")
        DOHLCV.columns = ["date", "open", "high", "low", "close", "volume"]
        DOHLCV.ta.adjusted = "adj_close"
        OHLCV = DOHLCV.iloc[:, [1, 2, 3, 4, 5]]
        OHLCV.set_index(pd.DatetimeIndex(DOHLCV["date"]), inplace=True)
        OHLCV = OHLCV.astype("float64")
        return OHLCV

    def compute_indicators(self, ohlcv, indicators=[]):

        c = ohlcv["close"]
        h = ohlcv["high"]
        l = ohlcv["low"]
        v = ohlcv["volume"]

        cs = ta.vwema(h, v, length=3)
        cs.rename("csup", inplace=True)

        cm = ta.vwema(c, v, length=3)
        cm.rename("cmed", inplace=True)

        ci = ta.vwema(l, v, length=3)
        ci.rename("cinf", inplace=True)

        macd = ta.macd(c)
        rsi = ta.rsi(c, length=7)

        macd = ta.macd(c)
        macd_h = macd["MACDh_12_26_9"]
        # %%
        macd_mean = macd.mean()
        macd_std = macd.std()

        macd = (macd - macd_mean) / macd_std
        macd_h = macd["MACDh_12_26_9"]

        D1h = macd_h.shift(1) - macd_h
        D1h = D1h.rename("D1h")

        D2h = D1h.shift(1) - D1h
        D2h = D2h.rename("D2h")

        df = pd.concat([cs, ci, c, cm, v, macd, rsi, D1h, D2h], axis=1)

        return df


# %%
import pandas_ta

pandas_ta.Category["overlap"][""]
df.ta.indicators()
