# %%
"""
A short description.

A bit longer description.

Args:
    variable (type): description

Returns:
    type: description

Raises:
    Exception: description

"""

# import json
from operator import itemgetter
from grabber import DataGrabber

import logging
import os
import time
import dateparser
import threading
import numpy as np
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from unicorn_binance_rest_api.unicorn_binance_rest_api_manager import (
    BinanceRestApiManager as Client,
)
from unicorn_binance_rest_api.unicorn_binance_rest_api_helpers import (
    interval_to_milliseconds,
)
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)

# %%


def name_trader(strategy):
    return strategy.name + "_" + strategy.symbol + "_" + strategy.timeframe


# %%

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

# %%


formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# %%


class Manager:
    """
    A short description.

    A bit longer description.

    Args:
        variable (type): description

    Returns:
        type: description

    Raises:
        Exception: description

    """

    def __init__(self, api_key, api_secret):
        self.traders = {}
        self.client = Client(
            api_key=api_key,
            api_secret=api_secret,
        )
        self.bwsm = BinanceWebSocketApiManager(
            output_default="UnicornFy", exchange="binance.com-futures"
        )

    def start_trader(self, strategy):

        trader_name = name_trader(strategy)

        if trader_name not in self.get_traders():
            trader = ATrader(self, strategy)
            trader.start_new_stream()
            self.traders[trader.name] = trader
            return trader
        else:
            print("Redundant trader. No new thread was created.\n")
            print("Try changing some of the strategy's parameters.\n")

    def get_traders(self):
        return list(self.traders.items())

    def close_traders(self, traders=None):
        """
        fecha todos os traders e todas as posições; pra emerg
        """
        if traders is None:
            # fecha todos os traders
            for name, trader in self.get_traders():
                trader.stop()
        else:
            # fecha só os passados como argumento
            pass
        pass

    def stop(self):
        self.close_traders()
        self.bwsm.stop_manager_with_all_streams()

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
    """
    A short description.

    A bit longer description.

    Args:
        variable (type): description

    Returns:
        type: description

    Raises:
        Exception: description

    """

    def __init__(self, manager, strategy):

        self.manager = manager
        self.bwsm = manager.bwsm
        self.client = manager.client
        self.strategy = strategy
        self.name = name_trader(strategy)
        self.data = []
        self.profits = []
        self.cum_profit = 0

        self.stoploss_parameter = strategy.stoploss_parameter
        self.take_profit = strategy.take_profit
        self.entry_window = strategy.entry_window
        self.exit_window = strategy.exit_window
        self.macd_params = strategy.macd_params

        self.keep_running = True
        self.stream_id = None
        self.stream_name = None

        self.grabber = DataGrabber(self.client)
        self.data_window = self._get_initial_data_window()

        self.init_time = time.time()

        self.is_positioned = False
        self.entry_price = None
        self.entry_time = None
        # logging_init_time = pd.to_datetime(self.init_time, unit="s", utc=False)
        self.logger = setup_logger(
            f"{self.name}-logger", f"{self.name}-{self.init_time}.log"
        )

    def process_stream_data(self):

        while self.keep_running:
            time.sleep(1)
            if self.bwsm.is_manager_stopping():
                exit(0)

            oldest_stream_data_from_stream_buffer = (
                self.bwsm.pop_stream_data_from_stream_buffer(self.stream_name)
            )

            if oldest_stream_data_from_stream_buffer is False:
                time.sleep(0.01)
            # elif oldest_stream_data_from_stream_buffer["event_type"] == "kline":
            else:
                try:
                    if oldest_stream_data_from_stream_buffer["event_type"] == "kline":

                        kline = oldest_stream_data_from_stream_buffer["kline"]

                        now = time.time()
                        kline_time = pd.to_datetime(now, unit="s", utc=True)
                        # start_time = pd.to_datetime(
                        #     kline["kline_close_time"], unit="ms"
                        # )
                        # print(kline_time)

                        o = float(kline["open_price"])
                        h = float(kline["high_price"])
                        l = float(kline["low_price"])
                        c = float(kline["close_price"])
                        v = float(kline["base_volume"])

                        num_trades = int(kline["number_of_trades"])
                        is_closed = bool(kline["is_closed"])

                        last_index = self.data_window.index[-1]

                        dohlcv = pd.DataFrame(
                            np.atleast_2d(np.array([kline_time, o, h, l, c, v])),
                            columns=[
                                "date",
                                "open",
                                "high",
                                "low",
                                "close",
                                "volume",
                            ],
                            index=[last_index],
                        )
                        ohlcv = dohlcv.drop(columns="date")
                        # print(dohlcv)

                        tf_as_seconds = (
                            interval_to_milliseconds(self.strategy.timeframe) * 0.001
                        )

                        # print(tf_as_seconds)

                        new_close = ohlcv.close
                        self.data_window.close.update(new_close)

                        macd = self.grabber.compute_indicators(
                            self.data_window.close, **self.strategy.macd_params
                        )
                        # print(macd)
                        date = dohlcv.date

                        new_row = pd.concat(
                            [date, macd.tail(1)],
                            axis=1,
                        )

                        # print(new_row)

                        if len(self.data) > 0:
                            self.data[0].update(new_row)
                        else:
                            self.data.append(new_row)

                        # print(f"{self.data[0]} \n {self.data_window.tail(1)}")
                        # print(self.data[0] == self.data_window.tail(1))
                        """
                        Testar pelas condiçoes, independentemente do tempo
                        """
                        # self.act_on_signal(self)

                        # print(int(now - self.init_time))

                        if int(now - self.init_time) >= tf_as_seconds / 1:

                            # self.data_window = self.data_window.drop(
                            #    self.data_window.iloc[[0]].index
                            # )
                            self.data_window.drop(index=[0], axis=0, inplace=True)
                            self.data_window = self.data_window.append(
                                new_row, ignore_index=True
                            )
                            # self.logger.info(
                            #     f"new window added:\n {self.data_window.tail(2)}"
                            # )
                            self.init_time = time.time()

                        else:
                            # self.data_window.iloc[[-1]] = new_row
                            self.data_window.update(new_row)

                except:
                    pass

    def start_new_stream(self):

        channel = "kline" + "_" + self.strategy.timeframe
        market = self.strategy.symbol

        stream_name = channel + "@" + market

        stream_id = self.bwsm.create_stream(
            channel, market, stream_buffer_name=stream_name
        )

        worker = threading.Thread(
            target=self.process_stream_data,
            args=(),
        )
        worker.setDaemon(True)
        worker.start()

        self.stream_name = stream_name
        self.worker = worker
        self.stream_id = stream_id

    def stop(self):
        self.keep_running = False
        self.bwsm.stop_stream(self.stream_id)
        del self.manager.traders[self.name]
        # self.worker._delete()

    def is_alive(self):
        return self.worker.is_alive()

    def _get_initial_data_window(self):
        klines = self.grabber.get_data(
            symbol=self.strategy.symbol,
            tframe=self.strategy.timeframe,
            limit=2 * self.macd_params["slow"],
        )
        last_kline_row = self.grabber.get_data(
            symbol=self.strategy.symbol, tframe=self.strategy.timeframe, limit=1
        )
        klines = klines.append(last_kline_row, ignore_index=True)

        # c = klines.close
        date = klines.date

        df = self.grabber.compute_indicators(
            klines.close, is_macd=True, **self.strategy.macd_params
        )
        # print(df)
        # macd = ta.macd(c)
        # df = pd.concat([date, klines, macd], axis=1)
        df = pd.concat([date, df], axis=1)
        return df

    def act_on_signal(self):
        """
        aqui eu tenho que
        1) mudar o sinal de entrada pra incluir as duas direçoes
        2) ver se realmente preciso dessas funçoes ou se dá pra deixar
        toda a operação dentro dessa mesma
        3) de qualquer forma, essa é a função que faz os trades, efetivamente
        """
        if self.is_positioned:
            if self.strategy.stoploss_check(self.data_window, self.entry_price):

                self.is_positioned = False
                exit_price = self.data_window.close.tail(1)
                exit_time = self.data_window.date.tail(1)

                profit = exit_price - self.entry_price
                percentual_profit = (
                    (exit_price - self.entry_price) / self.entry_price
                ) * 100

                resolution_time = exit_time - self.entry_time

                self.profits.append([profit, percentual_profit, resolution_time])
                self.cum_profit += percentual_profit
                self.logger.info(
                    f"""STOP-LOSS: E:{self.entry_price} - X:{exit_price}.
                                absΔ: {profit};
                                %Δ: {percentual_profit}%;
                                Δt: {res_time}.
                                cumulative profit: {self.cum_profit}.
                                running time: """
                )

            elif self.strategy.exit_signal(self.data_window, self.entry_price):

                self.is_positioned = False
                exit_price = self.data_window.close.tail(1)
                exit_time = self.data_window.date.tail(1)

                profit = exit_price - self.entry_price
                percentual_profit = (
                    (exit_price - self.entry_price) / self.entry_price
                ) * 100

                resolution_time = exit_time - self.entry_time

                self.profits.append([profit, percentual_profit, resolution_time])
                self.cum_profit += percentual_profit
                self.logger.info(
                    f"""PROFIT: E:{self.entry_price} - X:{exit_price}.
                                absΔ: {profit};
                                %Δ: {percentual_profit}%;
                                Δt: {res_time}.
                                cumulative profit: {self.cum_profit}.
                                running time: """
                )
        else:
            if self.strategy.entry_signal(self.data_window):
                self.is_positioned = True
                self.entry_price = self.data_window.close.tail(1)
                self.entry_time = self.data_window.date.tail(1)
                self.logger.info(f"ENTRY: E:{self.entry_price} at t:{self.entry_time}")

    def live_plot(self):

        fig = plt.figure()
        title = f"live {self.strategy.symbol} price @ binance.com"

        fig.canvas.set_window_title(title)
        ax = fig.add_subplot(1, 1, 1)

        def animate(i):

            data = self.data_window

            xs = data.date
            ys = data.close
            ax.clear()
            ax.plot(xs, ys, "k")
            plt.xticks(rotation=45, ha="right")
            plt.subplots_adjust(bottom=0.30)
            plt.title(title)
            plt.ylabel("USDT Value")

        ani = animation.FuncAnimation(fig, animate, interval=1)
        plt.show()


# %%


class Strategy:
    """
    A short description.

    A bit longer description.

    Args:
        variable (type): description

    Returns:
        type: description

    Raises:
        Exception: description

    """

    def __init__(
        self,
        name,
        symbol,
        timeframe,
        stoploss_parameter,
        take_profit,
        entry_window,
        exit_window,
        macd_params={"fast": 12, "slow": 26, "signal": 9},
    ):
        self.name = name
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
            (self.data_window.closes / entry_price - 1) * 100
            >= self.take_profit  # pelo menos `take_profit` de lucro
        ) and (np.alltrue(data_window.histogram.tail(self.exit_window) > 0)):
            return True
        else:
            return False

    def stoploss_check(self, data_window, entry_price):

        return (data_window.closes / entry_price - 1) * 100 <= self.stoploss_parameter


# manager = Manager(api_key, api_secret)

# %%

# params = {"fast": 7, "slow": 14, "signal": 5}

# strategy = Strategy("macd", "ethusdt", "1m", -0.33,
#                    3.5, 2, 2, macd_params=params)

# %%

# trader = manager.start_trader(strategy)
#
# trader.worker.daemon
# time.sleep(5)
# trader.live_plot()
# time.sleep(15)
# data = trader.data
# trader.stop()
# %%

if __name__ == "__main__":

    manager = Manager(api_key, api_secret)
    params = {"fast": 7, "slow": 14, "signal": 5}

    # strategy1 = Strategy("macd", "ethusdt", "1m", -0.33, 3.5, 2, 2, macd_params=params)

    # strategy2 = Strategy("macd", "bnbusdt", "1m", -0.33, 3.5, 2, 2, macd_params=params)

    strategy1 = Strategy("macd", "ethusdt", "1m", -0.2, 1.5, 2, 1)
    strategy2 = Strategy("macd", "bnbusdt", "1m", -0.2, 1.5, 2, 1)
    strategy3 = Strategy("macd", "btcusdt", "1m", -0.2, 1.5, 2, 1)

    trader1 = manager.start_trader(strategy1)
    time.sleep(10)
    trader2 = manager.start_trader(strategy2)
    time.sleep(10)
    trader3 = manager.start_trader(strategy3)

# %%

# manager.stop()
# %%

# %%

# trader1.stop()
# trader1.is_alive()
# manager.traders
# trader2.stop()
# trader2.is_alive()

# %%
