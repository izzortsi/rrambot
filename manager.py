# %%
import os
import time
import pandas as pd
from binance import ThreadedWebsocketManager
from binance.client import Client
from grabber import DataGrabber
import pandas_ta as ta
import numpy as np

# %%
KEY = os.getenv('API_USER')
SECRET = os.environ.get('API_PASSWORD')
api_key = ""
api_secret = ""


# %%

# %%
self.twm = ThreadedWebsocketManager(
        api_key=api_key, api_secret=api_secret)
futures_account_trades

class Manager:
    def __init__(self, api_key, api_secret):
        self.data = {}
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self.twm = ThreadedWebsocketManager(
            api_key=api_key, api_secret=api_secret)
        # start is required to initialise its internal loop
        self.twm.start()

    def start_trader(self, strategy):
        trader = ATrader(self, strategy)
        pass

    def get_traders(self):
        return list(self.data.keys())

    def close_traders(self, traders = None):
        """
        fecha todos os traders e todas as posições; pra emerg
        """
        if traders == None:
            #fecha todos os traders
            pass
        else:
            #fecha só os passados como argumento
            pass
        pass

    def performance_check(self):
        pass

    def market_overview(self):
        """
        isso aqui pode fazer bastante coisa, na verdade pode ser mais sensato
        fazer uma classe que faça as funções e seja invocada aqui.
        mas, em geral, a idéia é pegar várias métricas de várias coins, algo que
        sugira com clareza o sentimento do mercado. eventualmente, posso realmente
        usar ML ou alguma API pra pegar sentiment analysis do mercado
        """
        pass

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
        # self.last_mark_price = self.grabber.get_data(symbol=self.symbol, tframe = self.timeframe, limit = 1)
        # self.data_window.append(self.last_)
        #self.last_histogram = self.data_window.tail(1).histogram
        self.init_time = time.time()

        self.is_positioned = False
        self.entry_price = None

    def start_futures_stream(self, stream="bnbusdt_perpetual@continuousKline_1m"):
        # stream = f"{self.symbol}@markPrice@1s"
        self.stream_name = self.twm.start_futures_multiplex_socket(
            callback=self.handle_stream_message, streams=[stream]
        )
        return self.stream_name

    def handle_stream_message(self, msg):
        # print(f"message type: {msg['stream']}")
        # print(f"message type: {msg['data']['e']}")
        # self.data[f"{msg['stream']}"]=msg['data']['k']['c']
        tf_as_seconds = interval_to_milliseconds(
            self.strategy.timeframe) * 0.001

        now = time.time()
        new_row = self.grabber.trim_data(msg["data"]["k"]).compute_indicators()

        if int(now - self.init_time) >= tf_as_seconds:

            self.data_window = self.data_window.drop(
                self.data_window.iloc[[0]].index)

            self.data_window = self.data_window.append(new_row)

        else:
            self.data_window.iloc[[-1]] = new_row

        self.act_on_signal(self)

    def signal_from_strategy(self):
        pass

    def act_on_signal(self):
        """
        aqui eu tenho que
        1) mudar o sinal de entrada pra incluir as duas direçoes
        2) ver se realmente preciso dessas funçoes ou se dá pra deixar
        toda a operação dentro dessa mesma
        3) de qualquer forma, essa é a função que faz os trades, efetivamente
        """
        if self.is_positioned:
            if strategy.stoploss_check(self.data_window, self.entry_price):
                return stop_loss()
            elif strategy.exit_signal(self.data_window, self.entry_price):
                return take_profit()
        else:
            if strategy.entry_signal(self.data_window):
                return take_position()

        # if not bool(msg["data"]["k"]["x"]):
        #     new_row = self.grabber.trim_data(
        #         msg["data"]["k"]).compute_indicators()
        #     self.data_window.iloc[[-1]] = new_row
        # else:
        #     self.data_window = self.data_window.drop(
        #         self.data_window.iloc[[0]].index)
        #     self.data_window = self.data_window.append(new_row)

    # def handle_socket_message(self, msg):
    #     print(f"stream: {msg['stream']}")
    #     print(
    #         f"message type: {msg['data']['e']}, close: {msg['data']['k']['c']}, volume: {msg['data']['k']['v']}"
    #     )
    #     self.data[f"{msg['stream']}"] = msg["data"]["k"]["c"]

    def _get_initial_data_window(self):
        klines = self.grabber.get_data(
            symbol=self.symbol,
            tframe=self.timeframe,
            limit=2 * self.macd_params["window_slow"],
        )
        last_kline_row = self.grabber.get_data(
            symbol=self.symbol, tframe=self.timeframe, limit=1
        )
        klines = klines.append(last_kline_row, ignore_index=True)
        c = klines.close
        date = klines.date
        macd = ta.macd(c)
        df = pd.concat([date, c, macd], axis=1)
        return df


# %%
time.time()
# %%


class Strategy:
    def __init__(
        self,
        symbol,
        timeframe,
        stoploss_parameter,
        take_profit,
        entry_window,
        exit_window,
        macd_params={"window_slow": 26, "window_fast": 12, "window_sign": 9},
    ):
        self.symbol = symbol
        self.timeframe = timeframe
        self.stoploss_parameter = stoploss_parameter
        self.take_profit = take_profit
        self.entry_window = entry_window
        self.exit_window = exit_window
        self.macd_params = macd_params

    def entry_signal(self, data_window):

        if np.alltrue(data_window.histogram.tail(self.entry_window) < 0):
            return True
        else:
            return False

    def exit_signal(self, data_window, entry_price):

        if (
            (self.data_window.closes / entry_price - 1) *
            100 >= self.take_profit  # pelo menos `take_profit` de lucro
        ) and (
            np.alltrue(data_window.histogram.tail(self.exit_window) > 0)
        ):
            return True
        else:
            return False

    def stoploss_check(self, data_window, entry_price):

        return (
            (data_window.closes / entry_price - 1) *
            100 <= self.stoploss_parameter
        )


time.time()
# %%
manager = Manager(api_key, api_secret)
# bnbusdt_perpetual@continuousKline_1m
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

df = pd.DataFrame(np.random.rand(10, 10))
df.tail(1)
df.iloc[[-1]]
newrow = df.tail(1) * 2
df.iloc[[-1]] = newrowreturn "tp"
df.tail(1)

df.drop(0)


# %%

klines = klines.drop(klines.iloc[[0]].index)
klines

# %%


def interval_to_milliseconds(interval):
    """Convert a Binance interval string to milliseconds
    :param interval: Binance interval string 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str
    :return:
         None if unit not one of m, h, d or w
         None if string not in correct format
         int value of interval in milliseconds
    """
    ms = None
    seconds_per_unit = {"m": 60, "h": 60 * 60,
                        "d": 24 * 60 * 60, "w": 7 * 24 * 60 * 60}

    unit = interval[-1]
    if unit in seconds_per_unit:
        try:
            ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
        except ValueError:
            pass
    return ms
