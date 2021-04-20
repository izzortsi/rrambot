# from unicorn_binance_websocket_api.unicorn_bsm import (
#    BinanceWebSocketApiManager,
# )
import time
import os
import threading

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
            time.sleep(2)
            if self.bsm.is_manager_stopping():
                print("1")
                exit(0)
            oldest_stream_data_from_stream_buffer = (
                self.bsm.pop_stream_data_from_stream_buffer(
                    stream_buffer_name=self.stream
                )
            )

            if oldest_stream_data_from_stream_buffer is False:
                time.sleep(0.01)
                print("2")
            else:
                if oldest_stream_data_from_stream_buffer is not None:
                    try:
                        # print only the last kline
                        self.data.append(oldest_stream_data_from_stream_buffer)
                        print(f"{self.stream}: {oldest_stream_data_from_stream_buffer}")
                    except KeyError:
                        print(f"dict: {oldest_stream_data_from_stream_buffer}")
                    except TypeError:
                        print(f"raw_data: {oldest_stream_data_from_stream_buffer}")


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
