# %%
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import (
    BinanceWebSocketApiManager,
)
import time

# %%
api_key = ""
api_secret = ""

# %%
def book_ticker(msg):
    print("book_ticker: " + str(msg))


def order_status(msg):
    print("order_status: " + str(msg))


# %%

bwsm = BinanceWebSocketApiManager()

book_ticker_id = bwsm.create_stream("bookTicker", "bnbbusd", stream_buffer_name=True)

# %%
while True:
    msg = bwsm.pop_stream_data_from_stream_buffer(book_ticker_id)
    if msg:
        book_ticker(msg)
    time.sleep(2)
