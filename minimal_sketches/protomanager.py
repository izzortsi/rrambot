import time
from binance import ThreadedWebsocketManager

api_key = ""
api_secret = ""
symbol = "BNBUSDT"

# %%


class Manager:
    def __init__(self, api_key, api_secret):
        self.data = {}
        self.twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
        # start is required to initialise its internal loop
        self.twm.start()

    def start_stream(self, stream="bnbusdt@kline_1m"):
        stream_name = self.twm.start_multiplex_socket(
            callback=self.handle_socket_message, streams=[stream]
        )
        return stream_name

    def start_futures_stream(self, stream="bnbusdt_perpetual@continuousKline_15m"):
        stream_name = self.twm.start_futures_multiplex_socket(
            callback=self.handle_socket_multiplex_message, streams=[stream]
        )
        return stream_name

    def start_continuous_stream(self, stream="bnbusdt_perpetual@continuousKline_15m"):
        stream_name = self.twm.start_futures_multiplex_socket(
            callback=self.handle_socket_multiplex_message, streams=[stream]
        )
        return stream_name

    def handle_socket_multiplex_message(self, msg):
        print(f"stream: {msg['stream']}")
        print(
            f"message type: {msg['data']['e']}, close: {msg['data']['k']['c']}, volume: {msg['data']['k']['v']}"
        )
        self.data[f"{msg['stream']}"] = msg["data"]["k"]["c"]

    def handle_socket_message(self, msg):
        # print(f"stream: {msg['stream']}")
        print(
            f"message type: {msg['data']['e']}, close: {msg['data']['k']['c']}, volume: {msg['data']['k']['v']}"
        )
        self.data[f"{msg['stream']}"] = msg["data"]["k"]["c"]


# %%
manager = Manager(api_key, api_secret)
# bnbusdt_perpetual@continuousKline_1m
# %%
stream = manager.start_stream()

mstream = manager.start_futures_stream()

# %%
manager.twm.stop_socket(stream)
manager.twm.stop_socket(mstream)

# %%


def start_continuous_futures_kline_socket(self, callback: Callable) -> str:
    return self._start_async_socket(
        callback=callback, socket_name="futures_socket", params={}
    )


# %%

manager.twm.start_kline_socket(callback=manager.handle_socket_message, symbol=symbol)
# %%

manager.data
