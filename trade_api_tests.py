import unicorn_binance_rest_api as ubr
import unicorn_binance_websocket_api as ubw
import unicorn_binance_rest_api.unicorn_binance_rest_api_enums as enums
import os
import threading
import time

# %%


API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

brm = ubr.BinanceRestApiManager(api_key=API_KEY, api_secret=API_SECRET)
bwsm = ubw.BinanceWebSocketApiManager(
    output_default="UnicornFy", exchange="binance.com-futures"
)


# %%

channel = "kline_1m"
market = "ethusdt"

stream_name = channel + "@" + market

stream_id = bwsm.create_stream(channel, market, stream_buffer_name=stream_name)


# bwsm.stop_manager_with_all_streams()
# brm.get_asset_balance(asset="BRL")

# brm.futures_account_balance()
# brm.futures_change_margin_type(symbol="bnbusdt", marginType="ISOLATED")
# brm.futures_change_leverage(symbol="bnbusdt", leverage=5)

# brm.futures_create_order(
#     symbol="BNBUSDT",
#     side="SELL",
#     type="TAKE_PROFIT_MARKET",
#     stopPrice=450.10,
#     workingType="MARK_PRICE",
#     closePosition=True,
# )


data = []


def print_stream_data_from_stream_buffer(bwsm):
    while True:

        if bwsm.is_manager_stopping():
            exit(0)

        data_from_stream_buffer = bwsm.pop_stream_data_from_stream_buffer(stream_name)

        if data_from_stream_buffer is False:
            time.sleep(0.01)
        else:

            try:
                if data_from_stream_buffer["event_type"] == "kline":
                    # print(data_from_stream_buffer["event_type"])
                    global data
                    data.append(float(data_from_stream_buffer["kline"]["close_price"]))
            except:
                print(data_from_stream_buffer)


# %%
worker_thread = threading.Thread(
    target=print_stream_data_from_stream_buffer, args=(bwsm,)
)
worker_thread.start()


# %%
data
# %%
len(data)
# %%

last_price = data[-1]
last_price
position = brm.futures_position_information(symbol="ethusdt")
position
price = float(position[0]["entryPrice"])
price
f_tp_price = lambda price, tp, lev: f"{(price * (1+(tp/lev)/100)):.2f}"
f_sl_price = lambda price, sl, lev: f"{(price * (1-(sl/lev)/100)):.2f}"
# %%
brm.futures_get_open_orders(symbol="ethusdt")
# %%

lev = int(position[0]["leverage"])

sl = 0.2
# sl / 100
tp = 4
# tp / 100
tp_price = f_tp_price(price, tp, lev)
sl_price = f_sl_price(price, sl, lev)
tp_price
sl_price
# %%

tp_price = f_tp_price(last_price, tp, lev)
sl_price = f_sl_price(last_price, sl, lev)


# %%
brm.futures_coin_place_batch_order()
# %%
new_position = brm.futures_create_order(
    symbol="ETHUSDT",
    side="BUY",
    type="MARKET",
    quantity=0.002,
    priceProtect=True,
)

position = brm.futures_position_information(symbol="ethusdt")
price = float(position[0]["entryPrice"])
qty = position[0]["positionAmt"]
tp_price = f_tp_price(price, tp, lev)
sl_price = f_sl_price(price, sl, lev)

stop_order = brm.futures_create_order(
    symbol="ETHUSDT",
    side="SELL",
    type="STOP_MARKET",
    stopPrice=sl_price,
    workingType="MARK_PRICE",
    quantity=qty,
    reduceOnly=True,
    priceProtect=True,
    timeInForce="GTE_GTC",
)

brm.futures_create_order(
    symbol="ETHUSDT",
    side="SELL",
    type="TAKE_PROFIT_MARKET",
    stopPrice=tp_price,
    workingType="MARK_PRICE",
    quantity=qty,
    reduceOnly=True,
    priceProtect=True,
    timeInForce="GTE_GTC",
)

# %%


# %%


# %%


stop_order = brm.futures_create_order(
    symbol="ETHUSDT",
    side="SELL",
    type="STOP_MARKET",
    stopPrice=sl_price,
    workingType="MARK_PRICE",
    closePosition=True,
)

# %%

# %%

brm.futures_create_order(
    symbol="ETHUSDT",
    side="SELL",
    type="TAKE_PROFIT_MARKET",
    stopPrice=tp_price,
    workingType="MARK_PRICE",
    closePosition=True,
)
