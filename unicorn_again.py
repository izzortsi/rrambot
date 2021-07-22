# %%
from unicorn_binance_rest_api.unicorn_binance_rest_api_manager import (
    BinanceRestApiManager as Client,
)
import logging
import os

# for random filenames
# import random
# import string
# import datetime

#
# today_date = str(datetime.date.today())
#
# char_set = string.ascii_uppercase + string.ascii_lowercase
# log_filename = today_date.join(random.sample(char_set * 6, 8))
#

# https://docs.python.org/3/library/logging.html#logging-levels

logging.basicConfig(
    level=logging.DEBUG,
    filename=os.path.basename("__file__") + ".log",
    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
    style="{",
)

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

client = Client(api_key, api_secret, tld="com")
# %%

# get market depth
depth = client.get_order_book(symbol="BNBBTC")
print(f"{depth}")

# get all symbol prices
prices = client.get_all_tickers()
print(f"{prices}")
