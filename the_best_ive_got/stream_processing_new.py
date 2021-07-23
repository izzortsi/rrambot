# %%

from __future__ import print_function
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)
import time
import threading
import os
from operator import itemgetter

# %%

class StreamProcesser:
    def __init__(self, bwsm):
        self.bwsm = bwsm
        self.data_dict = {}
        self.keep_streaming = {}
        self.streams = {}

    def process_stream_data_from_stream_buffer(self, stream_name):
        print("print trades only")
        time.sleep(4)
        self.data_dict[stream_name] = []
        c = 0
        while self.keep_streaming[stream_name]:
            if self.bwsm.is_manager_stopping():
                exit(0)
            oldest_stream_data_from_stream_buffer = (
                self.bwsm.pop_stream_data_from_stream_buffer(stream_name)
            )
            if oldest_stream_data_from_stream_buffer is False:
                time.sleep(0.01)
            else:
                try:
                    data = itemgetter("symbol", "close_price", "base_volume", "is_closed")(
                        oldest_stream_data_from_stream_buffer["kline"]
                    )
                    self.data_dict[stream_name].append(data)
                    if c % 20 == 0:
                        print(data)
                        self.data_dict[stream_name] = []
                except Exception:
                    # not able to process the data? write it back to the stream_buffer
                    self.bwsm.add_to_stream_buffer(
                        oldest_stream_data_from_stream_buffer
                    )
            c += 1

    def start_new_stream(self, channel, market, stream_name=None):

        if stream_name is None:
            stream_name = market + "_" + channel

        self.streams[stream_name] = [
            self.bwsm.create_stream(
                channel,
                market,
                stream_buffer_name=stream_name,
            )
        ]

        worker_thread = threading.Thread(
            target=self.process_stream_data_from_stream_buffer, args=(stream_name,)
        )
        worker_thread.start()

        self.streams[stream_name].append(worker_thread)
        self.keep_streaming[stream_name] = True

        return {stream_name: self.streams[stream_name]}

    def end_stream(self, stream):
        stream_name = list(stream.keys())[0]
        values = list(stream.values())[0]
        self.keep_streaming[stream_name] = False
        self.bwsm.stop_stream(self.streams[stream_name][0])
        del self.streams[stream_name]


# %%
if __name__ == "__main__":

    bwsm = BinanceWebSocketApiManager(output_default="UnicornFy")

    markets = ["btcusdt", "ethusdt"]
    channels = ["kline_15m"]
    channel = "kline_15m"

    # %%
    processer = StreamProcesser(bwsm)
    # %%
    btcstream = processer.start_new_stream(channel, markets[0])
    ethstream = processer.start_new_stream(channel, markets[1])
    # %%
    sleep(15)

    # %%
    processer.streams["btcusdt_kline_15m"]
    # %%
    stream_name = list(btcstream.keys())[0]
    values = list(btcstream.values())[0]
    # %%
    stream_name
    values
    # %%


    bwsm.get_active_stream_list()

    # %%
    processer.end_stream(ethstream)
    processer.end_stream(btcstream)
    # %%
    processer.data_dict["btcusdt_kline_15m"]
    processer.data_dict["ethusdt_kline_15m"]

    # %%
    processer.data_dict

# %%
