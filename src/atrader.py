from src import *
from src.grabber import DataGrabber


class ATrader:
    def __init__(self, manager, strategy, symbol, leverage=1):

        self.manager = manager
        self.bwsm = manager.bwsm
        self.client = manager.client
        self.strategy = strategy
        self.symbol = symbol
        self.leverage = leverage
        self.name = name_trader(strategy, self.symbol)
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
        self.data = None

        self.start_time = time.time()  # wont change, used to compute uptime
        self.init_time = time.time()
        self.now = time.time()

        self.is_positioned = False
        self.entry_price = None
        self.entry_time = None
        self.last_price = None
        self.now_time = None
        self.uptime = None

        self.logger = setup_logger(
            f"{self.name}-logger", f"logs/{self.name}-{self.init_time}.log"
        )

    def stop(self):
        self.keep_running = False
        self.bwsm.stop_stream(self.stream_id)
        del self.manager.traders[self.name]
        # self.worker._delete()

    def is_alive(self):
        return self.worker.is_alive()

    def status(self):
        status = (
            self.is_alive(),
            self.is_positioned,
        )
        print(
            f"""uptime: {pd.to_datetime(self.now) - pd.to_datetime(self.start_time)};
              Δ%*leverage: {to_percentual(self.last_price, self.entry_price) * self.leverage}
              leverage: {self.leverage};
              status: Alive? Positioned? {status}
              """
        )
        # print(f"Is alive? {status[0]}; Is positioned? {status[1]}")
        return status

    def _get_initial_data_window(self):
        klines = self.grabber.get_data(
            symbol=self.symbol,
            tframe=self.strategy.timeframe,
            limit=2 * self.macd_params["slow"],
        )
        last_kline_row = self.grabber.get_data(
            symbol=self.symbol, tframe=self.strategy.timeframe, limit=1
        )
        klines = klines.append(last_kline_row, ignore_index=True)

        date = klines.date

        df = self.grabber.compute_indicators(
            klines.close, is_macd=True, **self.strategy.macd_params
        )

        df = pd.concat([date, df], axis=1)
        return df

    def _start_new_stream(self):

        channel = "kline" + "_" + self.strategy.timeframe
        market = self.symbol

        stream_name = channel + "@" + market

        stream_id = self.bwsm.create_stream(
            channel, market, stream_buffer_name=stream_name
        )

        worker = threading.Thread(
            target=self._process_stream_data,
            args=(),
        )
        worker.setDaemon(True)
        worker.start()

        self.stream_name = stream_name
        self.worker = worker
        self.stream_id = stream_id

    def _process_stream_data(self):

        while self.keep_running:
            time.sleep(1)
            if self.bwsm.is_manager_stopping():
                exit(0)

            oldest_stream_data_from_stream_buffer = (
                self.bwsm.pop_stream_data_from_stream_buffer(self.stream_name)
            )

            if oldest_stream_data_from_stream_buffer is False:
                time.sleep(0.01)

            else:
                try:
                    if oldest_stream_data_from_stream_buffer["event_type"] == "kline":

                        kline = oldest_stream_data_from_stream_buffer["kline"]

                        self.now = time.time()
                        kline_time = pd.to_datetime(self.now, unit="s", utc=False)

                        o = float(kline["open_price"])
                        h = float(kline["high_price"])
                        l = float(kline["low_price"])
                        c = float(kline["close_price"])
                        v = float(kline["base_volume"])

                        num_trades = int(kline["number_of_trades"])
                        is_closed = bool(kline["is_closed"])

                        last_index = self.data_window.index[-1]

                        self.last_price = c
                        self.now_time = kline_time

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

                        new_close = ohlcv.close
                        self.data_window.close.update(new_close)

                        macd = self.grabber.compute_indicators(
                            self.data_window.close, **self.strategy.macd_params
                        )

                        date = dohlcv.date

                        new_row = pd.concat(
                            [date, macd.tail(1)],
                            axis=1,
                        )

                        if (
                            int(self.now - self.init_time)
                            >= tf_as_seconds / self.manager.rate
                        ):

                            self.data_window.drop(index=[0], axis=0, inplace=True)
                            self.data_window = self.data_window.append(
                                new_row, ignore_index=True
                            )

                            self.init_time = time.time()

                        else:
                            self.data_window.update(new_row)

                            self.data = self.data_window.tail(
                                self.strategy.macd_params["signal"]
                            )

                        self.uptime = pd.to_datetime(self.now) - pd.to_datetime(
                            self.start_time
                        )

                        self._act_on_signal()

                        if int(self.now - self.start_time) % 60 == 0:
                            self.logger.info(
                                f"""uptime: {self.uptime};
                                      Δ%*leverage: {to_percentual(self.last_price, self.entry_price)*self.leverage};
                                      leverage: {self.leverage};
                                      status: Alive? Positioned? {self.status()}
                                      """
                            )

                except:
                    pass

    def _act_on_signal(self):
        """
        aqui eu tenho que
        1) mudar o sinal de entrada pra incluir as duas direçoes
        2) essa é a função que faz os trades, efetivamente. falta isso
        """

        if self.is_positioned:
            # print(
            #     self.strategy.stoploss_check(self, self.data_window, self.entry_price)
            # )
            if self.strategy.stoploss_check(self, self.data_window, self.entry_price):

                exit_price = self.data_window.close.values[-1]
                exit_time = self.data_window.date.values[-1]

                profit = (exit_price - self.entry_price) * self.leverage
                percentual_profit = (
                    ((exit_price - self.entry_price) / self.entry_price)
                    * 100
                    * self.leverage
                )

                resolution_time = exit_time - self.entry_time

                self.profits.append([profit, percentual_profit, resolution_time])
                self.cum_profit += percentual_profit
                self.logger.info(
                    f"""STOP-LOSS: (E:{self.entry_price} - X:{exit_price}) x L:{self.leverage}.
                                Δabs: {profit};
                                Δ%: {percentual_profit}%;
                                Δt: {res_time}.
                                cumulative profit: {self.cum_profit}.
                                uptime: {self.uptime}"""
                )

                self.is_positioned = False

            elif self.strategy.exit_signal(self, self.data_window, self.entry_price):

                exit_price = self.data_window.close.values[-1]
                exit_time = self.data_window.date.values[-1]

                profit = exit_price - self.entry_price
                percentual_profit = (
                    (exit_price - self.entry_price) / self.entry_price
                ) * 100

                resolution_time = exit_time - self.entry_time

                self.profits.append([profit, percentual_profit, resolution_time])
                self.cum_profit += percentual_profit
                self.logger.info(
                    f"""PROFIT: (E:{self.entry_price} - X:{exit_price}) x L:{self.leverage}.
                                Δabs: {profit};
                                Δ%: {percentual_profit}%;
                                Δt: {res_time}.
                                cumulative profit: {self.cum_profit}.
                                uptime: {self.uptime}"""
                )

                self.is_positioned = False
        else:
            if self.strategy.entry_signal(self.data_window):
                self.is_positioned = True
                self.entry_price = self.data_window.close.values[-1]
                self.entry_time = self.data_window.date.values[-1]
                self.logger.info(f"ENTRY: E:{self.entry_price} at t:{self.entry_time}")

    def live_plot(self):

        fig = plt.figure()
        title = f"live {self.symbol} price @ binance.com"

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
