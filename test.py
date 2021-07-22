import os
import time
import pandas as pd
from binance import ThreadedWebsocketManager, BinanceSocketManager
from binance.client import Client
from binance.helpers import round_step_size
from grabber import DataGrabber
import pandas_ta as ta
import numpy as np
import json
import asyncio
from binance import AsyncClient


async def main():
    api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    client = await AsyncClient.create(api_key, api_secret)
    lkey = client.futures_stream_get_listen_key()
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.user_socket()
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)

    await client.close_connection()


# %%client.futures_change_leverage(symbol="ETHUSDT", leverage = leverage)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
