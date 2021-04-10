##
from binance.websockets import BinanceSocketManager
from binance.client import Client
from binance.enums import *
##
from typing import Union, Callable
numeric = Union[int, float]
##
from grabber import *
##

#parametros

KEY = ""
SECRET = ""
symbol="ETHUSDT"
tframe="30m"
fromdate="1 day ago"
todate = None

##
client=Client(api_key=KEY, api_secret=SECRET)
##
grab = Grabber(client)
##
df = grab.compute_indicators()

##

def format_to_precision(amount, precision=8):
    return "{:0.0{}f}".format(amount, precision)

def strategy(data, E: Callable, X: Callable, S = False, test = True) -> tuple:

    price = data["close"]
    time = data.index[0]
    I = data[:, data.columns != "close"] #get all indicators

    Entry = None
    eXit = None

    if (S and X(I)):

        #ordem de venda
        #aqui vai ser order = ...
        #e if (order["status"] == "FILLED") return (order["orderId"], order["transactTime"], order["price"])
        #else tem que ver issae
        sold_at = float(price)
        eXit = (time, sold_at)
        profit = sold_at - bought_at
        print(f"vendeu a {price} em {time}. Diferença de: {profit}. ")
        S = not(S)
        return (profit, S) #tem que ver melhor que que precisa retornar
        bought_at
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

class ATrader:
    
    def __init__(self, client, strategy)