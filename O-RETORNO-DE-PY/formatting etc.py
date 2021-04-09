##
from binance.client import Client
from binance.enums import *
##
from decimal import *
from typing import Union, Callable
numeric = Union[int, float]
##
from grabber import *
##
client=Client(api_key="XQbT3UoAVCqSr72ivWA2gBnDHAaGuNfaYdfduBMCW3VxHol4rmOCF2w8M3vr0u37",
            api_secret="iJ05eftlARzIcR9CHYKU81qkM21MIgvgmk5pZNvJWYLdYUgB6cS9bRLjwqBVXrQ9")
##
grab = Grabber(client)
##
df = grab.compute_indicators()

##
symbol="ETHUSDT"
tframe="30m"
fromdate="1 day ago"
todate = None

##
order = client.create_test_order(
    symbol=symbol,
    side="BUY",
    type="MARKET",
    quoteOrderQty=10,
    recvWindow = 10000
    )
##
order
##
amount = 0.000234234
precision = 8

def format_to_precision(amount, precision=8):
    return "{:0.0{}f}".format(amount, precision)

##
avgprice = client.get_avg_price(symbol=symbol)
maxprice, minprice = float(avgprice["price"])*5, float(avgprice["price"])*0.2
print(avgprice, float(avgprice["price"])*5, float(avgprice["price"])*0.2)
##
info = client.get_symbol_info(symbol)
print(info)
##
print(info['filters'][2]['minQty'])
##
minprice <= float('0.00579321') <= maxprice
print(minprice, float('0.00579321'), maxprice)
##
getcontext()
getcontext().prec = 8
##
price = float(client.get_ticker(symbol="ETHUSDT")["lastPrice"])
qty = 10.5/1400.0
#qty = Decimal(qty)
formated_qty = format_to_precision(qty, precision=8)
print(format_to_precision(qty, precision=8))
##
balance = client.get_asset_balance(asset='USDT', recvWindow=8000)
print(balance['free'])
quantity = (float(balance['free']))/float(trades[0]['price'])*0.9995
print(quantity)
##
trades
##
order = client.create_test_order(
    symbol=symbol,
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=formated_qty,
    price='1400.0000',
    recvWindow=7000)
##
order
##
order = client.create_test_order(
    symbol=symbol,
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=info['filters'][2]['minQty'],
    price='0.00579321',
    recvWindow=7000)
##

order = client.order_limit_buy(
    symbol=symbol,
    quantity="0.000170",
    price='45000.000',
    recvWindow=7000)
##

def strategy(data, E: Callable, X: Callable, S: bool, test = True) -> tuple:

    price = data["close"]
    time = data.index[0]
    I = data[:, data.columns != "close"] #get all indicators

    Entry = None
    eXit = None

    if (S and X(I)):
        if test == True:
            order = client.create_test_order(
                symbol=symbol,
                side="BUY",
                type="MARKET",
                quoteOrderQty=10
                )
        else:
            #order = ...
            NotImplementedError

        transId, time, price = NotImplementedError #vende e retorna id da transação, hora e preço
        eXit = (time, price)
        print(f"vendeu a {price} em {time}. Diferença de: ")
        S = not(S)
        return (orderId, S) #tem que ver melhor que que precisa retornar
    elif (not(S) and E(I)):
        orderId, time, price = NotImplementedError #compra e retorna id da ordem, hora e preço
        Entry = (time, price)
        print(f"comprou a {price} em {time}")
        S = not(S)
    else:
        if check_for_stoploss(candle, I):
            print(f"vendeu a {price} em {time}. Diferença de: ")
            return (orderId, S) #tem que ver melhor que que precisa retornar


##

df.loc[:, df.columns != 'close']
##
