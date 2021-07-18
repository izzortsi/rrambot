##
import pandas as pd
import pandas_ta as ta

##
class DataGrabber:
    def __init__(self, client):
        self.client = client

    def get_data(
        self, symbol="BTCUSDT", tframe="1h", limit=None, startTime=None, endTime=None
    ):
        klines = self.client.futures_continous_klines(pair=symbol,
            interval=tframe,
            contractType="PERPETUAL",
            limit=limit,
            startTime=startTime,
            endTime=endTime,
        )
        return self.trim_data(klines)
        # replaced_fromdate = fromdate.replace(" ", "-")

    def trim_data(self, klines):

        df = pd.DataFrame(data=klines)
        DOHLCV = df.iloc[:, [0, 1, 2, 3, 4, 5]]
        dates = pd.to_datetime(DOHLCV[0], unit="ms")
        OHLCV = DOHLCV.iloc[:, [1, 2, 3, 4, 5]].astype("float64")
        #OHLCV.set_index(pd.DatetimeIndex(DOHLCV["date"], freq="infer"), inplace=True)
        DOHLCV = pd.concat([dates, OHLCV], axis=1)
        DOHLCV.columns = ["date", "open", "high", "low", "close", "volume"]
        return DOHLCV

    def compute_indicators(self, ohlcv, is_macd = True, indicators=[]):

        c = ohlcv["close"]
        h = ohlcv["high"]
        l = ohlcv["low"]
        v = ohlcv["volume"]

        if is_macd:
            macd = ta.macd(c)
            macd.rename(
                columns={
                    "MACD_12_26_9": "macd",
                    "MACDh_12_26_9": "histogram",
                    "MACDs_12_26_9": "signal",
                },
                inplace=True,
            )

            df = pd.concat([c, macd], axis=1)
            return df

        else:

            cs = ta.vwma(h, v, length=3)
            cs.rename("csup", inplace=True)

            cm = ta.vwma(c, v, length=3)
            cm.rename("cmed", inplace=True)

            ci = ta.vwma(l, v, length=3)
            ci.rename("cinf", inplace=True)

            df = pd.concat([cs, ci, c, cm, v], axis=1)

            return df


##
