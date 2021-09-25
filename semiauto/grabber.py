# %%
from binance.client import Client
import pandas as pd
import pandas_ta as ta
from semiauto.indicators import *

# %%


class DataGrabber:
    def __init__(self, client):
        self.client = client

    def get_data(self, symbol="BTCUSDT", timeframe="4h", fromdate="2 month ago"):
        klines = self.client.get_historical_klines(symbol, timeframe, fromdate)
        replaced_fromdate = fromdate.replace(" ", "-")
        return self.trim_data(klines)

    def trim_data(self, rdata):
        df = pd.DataFrame(data=rdata)
        DOHLCV = df.iloc[:, [0, 1, 2, 3, 4, 5]]
        DOHLCV[0] = pd.to_datetime(DOHLCV[0], unit="ms")
        DOHLCV.columns = ["date", "open", "high", "low", "close", "volume"]
        DOHLCV.ta.adjusted = "adj_close"
        OHLCV = DOHLCV.iloc[:, [1, 2, 3, 4, 5]]
        OHLCV.set_index(pd.DatetimeIndex(DOHLCV["date"]), inplace=True)
        OHLCV = OHLCV.astype("float64")
        return OHLCV

    def compute_indicators(self, ohlcv, N=2, indicators={}):

        c = ohlcv["close"]
        h = ohlcv["high"]
        l = ohlcv["low"]
        v = ohlcv["volume"]

        cs = ta.vwema(h, v, length=N)
        cs.rename("csup", inplace=True)

        cm = ta.vwema(c, v, length=N)
        cm.rename("cmed", inplace=True)

        ci = ta.vwema(l, v, length=N)
        ci.rename("cinf", inplace=True)

        mfi = ta.mfi(h, l, c, v, length=14)

        macd = ta.macd(c)

        def normalize(series):
            mean = series.mean()
            stdev = series.std()
            return (series - mean) / stdev

        # macd_mean = macd.mean()
        # macd_std = macd.std()

        macd_h = macd["MACDh_12_26_9"]

        macd = normalize(macd)

        print(macd_h.tail(3))
        print(macd.tail(3))

        D1h = macd_h.shift(1) - macd_h
        D1h = D1h.rename("D1h")
        D1h = normalize(D1h)
        D2h = D1h.shift(1) - D1h
        D2h = D2h.rename("D2h")
        D2h = normalize(D2h)
        df = pd.concat([cs, ci, c, cm, v, macd, mfi, D1h, D2h], axis=1)

        return df


# %%
