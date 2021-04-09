##
import pandas as pd
from binance.client import Client
##
# Load data

client = Client()
#klines = client.get_historical_klines("DOGEUSDT", "1h", "20 month ago")
#symbol, tframe, fromto = "ETHUSDT", "1h", "4 month ago"
symbol, tframe, fromto = "BTCUSDT", "1h", "4 month ago"
klines = klines = client.get_historical_klines(symbol, tframe, fromto)

##
df = pd.DataFrame(data = klines)
DOHLCV = df.iloc[:, [0, 1, 2, 3, 4, 5]]
DOHLCV.columns = ["date", "open", "high", "low", "close", "volume"]
series_len = len(DOHLCV.date)
##
timestamp = pd.to_datetime(DOHLCV.date, utc=True, unit='ms')
isotstamp = pd.Series(list(map(pd.Timestamp.isoformat, timestamp)))
isotstamp.name = "timestamp"
##

#series = pd.Series(["closes" for i in range(series_len)])
#series.name = "series"

labels = pd.Series(["wait" for i in range(series_len)], name="label")

##    
closes = DOHLCV.close.astype("float64")
closes.name = "value"
series_closes = pd.Series(["closes" for i in range(series_len)])
series_closes.name = "series"
closes_ts = pd.concat([series_closes, isotstamp, closes, labels], axis=1)
##

highs = DOHLCV.high.astype("float64")
highs.name = "value"
series_highs = pd.Series(["highs" for i in range(series_len)])
series_highs.name = "series"
highs_ts = pd.concat([series_highs, isotstamp, highs, labels], axis=1)

##

lows = DOHLCV.low.astype("float64")
lows.name = "value"
series_lows = pd.Series(["lows" for i in range(series_len)])
series_lows.name = "series"
lows_ts = pd.concat([series_lows, isotstamp, lows, labels], axis=1)
##

values = pd.concat([lows_ts, closes_ts, highs_ts], axis=0)

values.sort_values(by= "timestamp", inplace=True)
values
##
len(values.values)
##
#values = pd.DataFrame.append(lows_ts, closes_ts, highs_ts)

#values

##
#out_df = pd.concat([series, values, labels], axis=1)

##
#labels = pd.Series([None for i in range(series_len)], name="label")
#labels = pd.concat([labels, labels, labels], axis=0)
#labels[0] = 0
#labels[1] = 2
##
#out_df = pd.concat([values, labels], axis=1)

##
out_df = values

##
filename = f'{symbol}-{tframe}_{fromto}'
comp_method = "zip"
compression_opts = dict(method=comp_method, archive_name=f'{filename}.csv')
##

out_df.to_csv(f'{filename}.{comp_method}', index = False, compression=compression_opts)
out_df.to_csv(f'{filename}.csv', index = False)

##

##
