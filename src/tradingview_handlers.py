import threading
from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta


class ThreadedHandler:
    def __init__(self, symbol, tframes, rate):
        self.symbol = symbol
        self.tframes = tframes
        self.rate = rate
        self.signal = False
        self.handlers = self.make_handlers()
        self.threaded_handler = self.start_threaded_handler()

    def make_handlers(self):
        self.handlers = {}
        for tf in self.tframes:
            h_tf = TA_Handler(
                symbol=self.symbol,
                exchange="binance",
                screener="crypto",
                interval=tf,
                timeout=None,
            )
            self.handlers[f"h_{tf}"] = h_tf

    def check_signals(self):

        for handler_key in self.handlers:
            handler = self.handlers[f"{handler_key}"]
            analysis_tf = handler.get_analysis()
            recommendation = analysis_tf.summary["RECOMMENDATION"]
            if "BUY" not in recommendation:
                self.signal = False
            else:
                self.signal = True

    def start_threaded_handler(self):

        worker = threading.Thread(
            target=self.check_signals,
            args=(),
        )
        worker.setDaemon(True)
        worker.start()

        return worker
