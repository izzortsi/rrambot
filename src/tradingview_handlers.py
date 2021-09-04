# %%

import threading
from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta
import time


class ThreadedTAHandler(threading.Thread):
    def __init__(self, symbol, tframes, rate):
        threading.Thread.__init__(self)
        self.symbol = symbol
        self.tframes = tframes
        self.rate = rate
        self.signal = False
        self.handlers = {}
        self.make_handlers()
        #self.threaded_handler = self.start_threaded_handler()
        self.keep_alive = True
        self.daemon = True

    def run(self):
        while self.keep_alive:
            self.check_signals()
            # self.signals.append(self.signal)
            #print(self.signal)
            time.sleep(self.rate)

    def stop(self):
        self.keep_alive = False

    def make_handlers(self):

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
            #print(analysis_tf.summary)
            if "BUY" not in recommendation:
                self.signal = False
            else:
                self.signal = True

    # def start_threaded_handler(self):
    #
    #     worker = threading.Thread(
    #         target=self.check_signals,
    #         args=(),
    #     )
    #     worker.setDaemon(True)
    #     worker.start()
    #
    #     return worker
# %%
th = ThreadedTAHandler("bnbusdt", ["1m", "5m"], 5)
th.start()
th.isDaemon()
