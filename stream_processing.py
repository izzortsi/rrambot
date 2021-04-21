# from unicorn_binance_websocket_api.unicorn_bsm import (
#    BinanceWebSocketApiManager,
# )
import time
import os
import threading
from operator import itemgetter

# %%

# create instance of BinanceWebSocketApiManager
# bsm = BinanceWebSocketApiManager(exchange="binance.com", output_default="UnicornFy")

# btc_id = bsm.create_stream(
#    "kline_1m", "btcusdt", stream_label="btcusdt_1", output="UnicornFy"
# )
# %%
# bsm.create_stream('kline_1m', markets, stream_label="dict", output="dict")

# bsm.create_stream('kline_1m', markets, stream_label="raw_data", output="raw_data")


# %%
# btc_id
# %%
class StreamProcesser:
    def __init__(self, bsm, stream_name, data=[]):
        self.bsm = bsm
        self.stream_id = self.bsm.get_stream_id_by_label(stream_name)
        self.data = data
        self.keep_running = True
        self.stream = stream_name

    def process_stream(self):
        while self.keep_running:
            time.sleep(5)
            if self.bsm.is_manager_stopping():
                exit(0)
            oldest_stream_data_from_stream_buffer = (
                self.bsm.pop_stream_data_from_stream_buffer(self.stream)
            )

            if oldest_stream_data_from_stream_buffer is False:
                time.sleep(0.01)
            else:
                if oldest_stream_data_from_stream_buffer is not None:
                    try:
                        # print only the last kline
                        data = itemgetter("symbol", "close_price", "is_closed")(
                            oldest_stream_data_from_stream_buffer["kline"]
                        )
                        self.data.append(data)
                        print(f"{self.stream}: {data}")
                    except Exception:
                        # not able to process the data? write it back to the stream_buffer
                        self.bsm.add_to_stream_buffer(
                            oldest_stream_data_from_stream_buffer
                        )


# %%
# process_stream = StreamProcesser(bsm)
## %%
# worker_thread = threading.Thread(
#    target=process_stream.process_stream,
#    name=bsm.get_stream_label(btc_id),
# )
# worker_thread.start()
## %%
# process_stream.keep_running = False
#
