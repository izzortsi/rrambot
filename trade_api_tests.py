import unicorn_binance_rest_api as ubr
import unicorn_binance_websocket_api as ubw
import unicorn_binance_rest_api.unicorn_binance_rest_api_enums as enums
from unicorn_binance_rest_api.unicorn_binance_rest_api_exceptions import *
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


f_tp_price = lambda price, tp, lev: f"{(price * (1+(tp/lev)/100)):.2f}"
f_sl_price = lambda price, sl, lev: f"{(price * (1-(sl/lev)/100)):.2f}"
# %%

lev = 100

sl = 1
# sl / 100
tp = 5
# tp / 100
# tp_price = f_tp_price(price, tp, lev)
# sl_price = f_sl_price(price, sl, lev)
# tp_price
# sl_price

# %%

brm.futures_change_leverage(symbol="ethusdt", leverage=lev)
# %%

# %%
try:
    new_position = brm.futures_create_order(
        symbol="ETHUSDT",
        side="BUY",
        type="MARKET",
        quantity=0.002,
        priceProtect=True,
    )
except BinanceAPIException as error:
    print(type(error))
    print("positioning, ", error)
else:
    position = brm.futures_position_information(symbol="ethusdt")
    price = float(position[0]["entryPrice"])
    qty = position[0]["positionAmt"]
    tp_price = f_tp_price(price, tp, lev)
    sl_price = f_sl_price(price, sl, lev)
    tp_price
    sl_price

    try:
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
    except BinanceAPIException as error:
        if error.code == -2021:
            print(type(error))
            print("sl order, ", error)
            try:
                brm.futures_create_order(
                    symbol="ETHUSDT",
                    side="SELL",
                    type="MARKET",
                    quantity=0.002,
                    priceProtect=True,
                )
            except BinanceAPIError as error:
                print(type(error))
                print("sl order 2, ", error)
    else:
        try:
            tp_order = brm.futures_create_order(
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
        except BinanceAPIException as error:

            print(type(error))
            print("tp order, ", error)
# %%
tp_order2 = brm.futures_create_order(
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
tp_order2 = None
# %%
print(tp_order2)
# %%

new_position

# %%


stop_order["orderId"]
brm.futures_get_order(symbol="ethusdt", orderId=stop_order["orderId"])
brm.futures_cancel_all_open_orders

# %%

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
