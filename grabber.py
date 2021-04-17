##
import pandas as pd
import pandas_ta as ta
##
class Grabber:

    def __init__(self, client):
        self.client = client

    def get_data(self, symbol="BTCUSDT", tframe="1h", fromdate="3 day ago", todate = None):

        klines = self.client.get_historical_klines(symbol, tframe, fromdate, end_str=todate)
        self.klines = klines
        #replaced_fromdate = fromdate.replace(" ", "-")

    def trim_data(self, data = None):
        if data == None:
            data = self.klines
        df = pd.DataFrame(data = data)
        DOHLCV = df.iloc[:, [0, 1, 2, 3, 4, 5]]
        DOHLCV[0] = pd.to_datetime(DOHLCV[0], unit='ms')
        DOHLCV.columns = ["date", "open", "high", "low", "close", "volume"]
        OHLCV = DOHLCV.iloc[:, [1, 2, 3, 4, 5]]
        OHLCV.set_index(pd.DatetimeIndex(DOHLCV["date"]), inplace=True)
        OHLCV = OHLCV.astype('float64')
        self.ohlcv = OHLCV
        if data != self.klines:
            return self.ohlcv

    def compute_indicators(self, indicators=[]):

        c = self.ohlcv.pop("close")
        h = self.ohlcv.pop("high")
        l = self.ohlcv.pop("low")
        v = self.ohlcv.pop("volume")

        cs = ta.vwma(h, v, length=3)
        cs.rename("csup", inplace=True)

        cm = ta.vwma(c, v, length=3)
        cm.rename("cmed", inplace=True)

        ci = ta.vwma(l, v, length=3)
        ci.rename("cinf", inplace=True)

        df = pd.concat([cs, ci, c, cm, v], axis=1)

        return df
class GrabberMACD(Grabber):

    def compute_indicators(self, indicators=[]):

        c = self.ohlcv.pop("close")
        h = self.ohlcv.pop("high")
        l = self.ohlcv.pop("low")
        v = self.ohlcv.pop("volume")

        macd = ta.macd(c)
        macd.rename(columns={"MACD_12_26_9": "macd",
        "MACDh_12_26_9": "histogram",
        "MACDs_12_26_9": "signal"},
        inplace=True)

        df = pd.concat([c, macd], axis=1)

        return df


##


