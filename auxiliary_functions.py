import os
from unicorn_binance_rest_api import BinanceRestApiManager
from src import *

# %%


def make_client(new=True):
    key, secret = os.environ.get("API_KEY"), os.environ.get("API_SECRET")
    if not new:
        client = BinanceRestApiManager(api_key=key, api_secret=secret)
    else:
        client = BinanceRestApiManager(
            api_key=key, api_secret=secret, exchange="binance.com-futures"
        )
    return client, key, secret
