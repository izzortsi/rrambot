
# %%

import time
import pandas as pd
from binance import ThreadedWebsocketManager
from binance.client import Client
from grabber import DataGrabber
import pandas_ta as ta

 # %%

api_key = "tF8GCAOYQ6G8fqgiwPDv3cDGfPOJffrXpYUcgkcEY38UCTRxG8D7fblZwyOFoMEA"
api_secret = "J4Gp5w0jdg2LICtXt1yY41TXWTOyrWCifCSMdyGtfMgVMVNFVDClnSXV9Tvh7zRT"


# %%
client = Client(api_key=api_key, api_secret=api_secret)

toappend = pd.Series(float(client.futures_mark_price(symbol="BNBUSDT")["markPrice"]))
client.futures_symbol_ticker(symbol="BNBUSDT")
klines = DataGrabber(client).get_data(limit=10)
toappend = DataGrabber(client).get_data(limit=1)
klines = klines.append(toappend, ignore_index=True)

# %%


class Manager:
    def __init__(self, api_key, api_secret):
        self.data = {}
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self.twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
        # start is required to initialise its internal loop
        self.twm.start()

    def start_futures_stream(self, stream="bnbusdt_perpetual@continuousKline_1m"):
        stream_name = self.twm.start_futures_multiplex_socket(callback=self.handle_socket_message, streams=[stream])
        return stream_name

    def start_trader(self, strategy):
        pass

    def get_traders(self):
        return list(self.data.keys())

    def handle_socket_message(self, msg):
        print(f"stream: {msg['stream']}")
        print(f"message type: {msg['data']['e']}, close: {msg['data']['k']['c']}, volume: {msg['data']['k']['v']}")
        self.data[f"{msg['stream']}"]=msg['data']['k']['c']

# %%

class ATrader:
    def __init__(self, manager, strategy):

        self.client = manager.client
        self.twm = manager.twm

        self.symbol = strategy.symbol
        self.timeframe = strategy.timeframe
        self.stoploss_parameter = strategy.stoploss_parameter
        self.take_profit = strategy.take_profit
        self.entry_window = strategy.entry_window
        self.exit_window = strategy.exit_window
        self.macd_params = strategy.macd_params

        self.grabber = DataGrabber(self.client)
        self.data_window = self._get_initial_data_window()
        #self.last_mark_price = self.grabber.get_data(symbol=self.symbol, tframe = self.timeframe, limit = 1)
        #self.data_window.append(self.last_)
        self.last_macd = self.data_window.tail(1)
        self.init_time = None


    def start_futures_stream(self, stream="bnbusdt_perpetual@continuousKline_1m"):
        #stream = f"{self.symbol}@markPrice@1s"
        self.stream_name = self.twm.start_futures_multiplex_socket(callback=self.handle_mark_price_message, streams=[stream])
        return self.stream_name

    def handle_mark_price_message(self, msg):
        #print(f"message type: {msg['stream']}")
        #print(f"message type: {msg['data']['e']}")
        #self.data[f"{msg['stream']}"]=msg['data']['k']['c']
        self.last_mark_price = float(msg["p"])

    def handle_stream_message(self, msg):
        #print(f"message type: {msg['stream']}")
        #print(f"message type: {msg['data']['e']}")
        #self.data[f"{msg['stream']}"]=msg['data']['k']['c']
        if not bool(msg['data']['k']['x']):
            new_row = self.grabber.trim_data(msg["data"]["k"]).compute_indicators()
            self.data_window.iloc[[-1]] = new_row
        else:
            self.data_window = self.data_window.drop(self.data_window.iloc[[0]].index)
            self.data_window = self.data_window.append(new_row)


    def _get_initial_data_window(self):
        klines = self.grabber.get_data(symbol=self.symbol, tframe = self.timeframe, limit = 2*self.macd_params["window_slow"])
        last_kline_row = self.grabber.get_data(symbol=self.symbol, tframe = self.timeframe, limit = 1)
        klines = klines.append(last_kline_row, ignore_index=True)
        c = klines.close
        date = klines.date
        macd = ta.macd(c)
        df = pd.concat([date, c, macd], axis=1)
        return df

# %%

class Strategy:
    def __init__(self,
                symbol,
                timeframe,
                stoploss_parameter,
                take_profit,
                entry_window,
                exit_window,
                macd_params = {"window_slow": 26, "window_fast": 12, "window_sign": 9},
                ):
        self.symbol = symbol
        self.timeframe = timeframe
        self.stoploss_parameter = stoploss_parameter
        self.take_profit = take_profit
        self.entry_window = entry_window
        self.exit_window = exit_window
        self.macd_params = macd_params

    def entry_signal(self, i):

        if np.alltrue(self.histogram.iloc[:i].tail(self.n1) < 0):
            return True
        else:
            return False

    def exit_signal(self, i, buy_price):

        if (
            (self.closes.iloc[i] / buy_price - 1) * 100 >= self.take_profit
        ) and (  # pelo menos `take_profit` de lucro
            np.alltrue(self.histogram.iloc[:i].tail(self.n2) > 0)
        ):
            return True
        else:
            return False

    def stoploss_check(self, i, buy_price):
        return (self.closes.iloc[i] / buy_price - 1) * 100 <= self.stoploss_parameter

# %%
manager = Manager(api_key, api_secret)
#bnbusdt_perpetual@continuousKline_1m
manager
# %%
strategy = Strategy("BNBUSDT", "15m", -0.33, 3.5, 2, 2)

# %%
strategy
# %%

atrader = ATrader(manager, strategy)

# %%
atrader
# %%
stream = manager.start_stream()

mstream = manager.start_futures_stream()

# %%
manager.twm.stop_socket(stream)
manager.twm.stop_socket(mstream)

# %%

manager.data



# %%
import numpy as np

df = pd.DataFrame(np.random.rand(10, 10))
df.tail(1)
df.iloc[[-1]]
newrow = df.tail(1)*2
df.iloc[[-1]] = newrow
df.tail(1)

df.drop(0)


# %%

klines = klines.drop(klines.iloc[[0]].index)
klines
