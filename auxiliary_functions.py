import os
from unicorn_binance_rest_api import BinanceRestApiManager
from src import *
# %%

def make_client():
    key, secret = os.environ.get('API_KEY'), os.environ.get('API_SECRET')
    client = BinanceRestApiManager(api_key=key, api_secret=secret, exchange="binance.com-futures")
    return client, key, secret