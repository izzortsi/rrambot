import pandas as pd
import pandas_ta as ta
from binance.client import Client

def init(api_key="", api_secret=""):
    client = Client(api_key=api_key,
                    api_secret=api_secret)
    return client

def get_data(symbol="BTCUSDT", tframe="30m", fromdate="1 day ago", todate = None):
    
    klines = client.get_historical_klines(symbol, tframe, fromdate)
    replaced_fromdate = fromdate.replace(" ", "-")
    return klines

def trim_data(rawdata):

    df = pd.DataFrame(data = rawdata)
    DOHLCV = df.iloc[:, [0, 1, 2, 3, 4, 5]]
    DOHLCV[0] = pd.to_datetime(DOHLCV[0], unit='ms')
    DOHLCV.columns = ["date", "open", "high", "low", "close", "volume"]
    OHLCV = DOHLCV.iloc[:, [1, 2, 3, 4, 5]]
    OHLCV.set_index(pd.DatetimeIndex(DOHLCV["date"]), inplace=True)
    OHLCV = OHLCV.astype('float64')
    return OHLCV

def compute_indicators(client,symbol="BTCUSDT", tframe="30m", fromdate="1 day ago", todate = None, indicators=[]):

    klines = get_data(symbol=symbol, tframe=tframe, fromdate=fromdate, todate=todate)
    ohlcv = trim_data(klines)

    c = ohlcv.pop("close")
    h = ohlcv.pop("high")
    l = ohlcv.pop("low")
    v = ohlcv.pop("volume")
    
    cs = ta.vwma(h, v, length=3)
    cs.rename("csup", inplace=True)

    cm = ta.vwma(c, v, length=3)
    cm.rename("cmed", inplace=True)

    ci = ta.vwma(l, v, length=3)
    ci.rename("cinf", inplace=True)
    
    df = pd.concat([cs, ci, c, cm, v], axis=1)

    return df

