##
import pandas as pd
from grabber import Grabber
from binance.client import Client
##
# Load data

client = Client()
#klines = client.get_historical_klines("DOGEUSDT", "1h", "20 month ago")
#symbol, tframe, fromto = "ETHUSDT", "1h", "4 month ago"
symbol, tframe, fromto = "BTCUSDT", "1h", "2 month ago"

grabber = Grabber(client)
out_df = grabber.compute_indicators(fromdate=fromto)
##
#out_df
###
#tstamps = pd.Series(out_df.date, name="timestamps")
#out_df = pd.concat([tstamps, out_df], axis=0)
###
#out_df

##
filename = f'{symbol}-{tframe}_{fromto}'
comp_method = "zip"
compression_opts = dict(method=comp_method, archive_name=f'{filename}.csv')
##

out_df.to_csv(f'{filename}.{comp_method}', index = True, compression=compression_opts)
out_df.to_csv(f'{filename}.csv', index = True)

##

##
