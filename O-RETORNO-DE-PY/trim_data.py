##
import pandas as pd
import pandas_ta as ta
from binance.client import Client
##
# Load data

client = Client()
klines = client.get_historical_klines("BTCUSDT", "30m", "1 day ago")

def trim_data(rdata):
    df = pd.DataFrame(data = rdata)
    DOHLCV = df.iloc[:, [0, 1, 2, 3, 4, 5]]
    DOHLCV[0] = pd.to_datetime(DOHLCV[0], unit='ms')
    DOHLCV.columns = ["date", "open", "high", "low", "close", "volume"]
    OHLCV = DOHLCV.iloc[:, [1, 2, 3, 4, 5]]
    OHLCV.set_index(pd.DatetimeIndex(DOHLCV["date"]), inplace=True)
    OHLCV = OHLCV.astype('float64')
    return OHLCV


##
ohlcv = trim_data(klines)
##
# VWAP requires the DataFrame index to be a DatetimeIndex.
# Replace "datetime" with the appropriate column from your DataFrame

# Calculate Returns and append to the df DataFrame
ohlcv.ta.log_return(cumulative=True, append=True)

##
ohlcv.ta.percent_return(cumulative=True, append=True)
##
# New Columns with results
ohlcv.columns

# Take a peek
ohlcv.tail()

# vv Continue Post Processing vv
# #

# #
