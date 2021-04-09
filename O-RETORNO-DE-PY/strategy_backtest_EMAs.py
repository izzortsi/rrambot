##
from binance.client import Client
from grabber import *
import numpy as np
##

#parametros

API_KEY = "XQbT3UoAVCqSr72ivWA2gBnDHAaGuNfaYdfduBMCW3VxHol4rmOCF2w8M3vr0u37"
API_SECRET = "iJ05eftlARzIcR9CHYKU81qkM21MIgvgmk5pZNvJWYLdYUgB6cS9bRLjwqBVXrQ9"
symbol="BTCUSDT"
tframe="5m"
fromdate="1 day ago"
todate = None

##
class GrabberEMA(Grabber):

    def compute_indicators(self, symbol="BTCUSDT", tframe="30m", fromdate="1 day ago", todate = None, indicators=[]):

        klines = self.get_data(symbol=symbol, tframe=tframe, fromdate=fromdate, todate=todate)
        ohlcv = self.trim_data(klines)

        c = ohlcv.pop("close")
        h = ohlcv.pop("high")
        l = ohlcv.pop("low")
        v = ohlcv.pop("volume")

        ema25 = ta.ema(c, length=25)
        ema25.rename("ema25", inplace=True)

        ema50 = ta.ema(c, length=50)
        ema50.rename("ema50", inplace=True)

        ema100 = ta.ema(c, length=100)
        ema100.rename("ema100", inplace=True)

        df = pd.concat([c, ema25, ema50, ema100], axis=1)

        return df
    

##
client = Client(api_key=API_KEY, api_secret=API_SECRET)
grab = GrabberEMA(client)
##

df = grab.compute_indicators(symbol=symbol, tframe=tframe, fromdate=fromdate, todate=todate)
##

##

##
class Backtester:

    def __init__(self, client, df, E, X):
        self.client = client
        self.df = df
        self.E = E
        self.X = X
        self.S = False
        self.Ops = []
        self.Entry = [None, None]
        self.eXit = [None, None]
        self.tail = 25

    def strategy(self, dates, prices, indicators):

        price = prices.iloc[-1]

        t0, buy_price = self.Entry

        #if (self.S and self.X(price, I)):
        if (self.S and self.X(price, buy_price)):
            #ordem de venda
            #aqui vai ser order = ...
            #e if (order["status"] == "FILLED") return (order["orderId"], order["transactTime"], order["price"])
            #else tem que ver issae
            sell_price = float(price)
            eXit = [time, sell_price]
            profit = sell_price - buy_price
            res_time = str(time - t0)
            print(f"vendeu a {sell_price} em {time}. Diferença de: {profit}. Tempo de resolução: {res_time} ")
            self.S = not(self.S)

            return self.Entry, self.eXit, profit, res_time, self.S #tem que ver melhor que que precisa retornar

        elif (not(self.S) and self.E(prices, indicators, self.tail)):

            self.Entry = [time, price]
            print(f"comprou a {price} em {time}")
            self.S = not(self.S)
            return
        else:
            if self.S and stoploss_check(price, I):
                sell_price = float(price)
                eXit = [time, sell_price]
                profit = sell_price - buy_price
                res_time = str(time - t0)
                print(f"Stop-loss: vendeu a {sell_price} em {time}. Diferença de: {profit}. Tempo de resolução: {res_time} ")
                self.S = not(self.S)
                return self.Entry, self.eXit, profit, res_time, self.S

            #if check_for_stoploss(price, I):
            #    print(f"vendeu a {price} em {time}. Diferença de: ")
            #    return (orderId, S) #tem que ver melhor que que precisa retornar

    def backtest(self):

        prices = self.df["close"]
        indicators = self.df.loc[:, self.df.columns != "close"]
        dates = prices.index

        dataset_size = len(dates)
        i = 100 + self.tail

        while (i <= dataset_size - 1):
            #print(self.S)
            action = self.strategy(dates, prices, indicators)

            if action != None:
                self.Ops.append(action[:-1])

            i += 1

        total_profit = 0
        for op in self.Ops:
            
            total_profit += op[2]

        info = client.get_ticker(symbol=symbol)
        ethprice = float(info["lastPrice"])
        print(f"Lucro aproximado em USD: {total_profit/ethprice}")

        return total_profit


##
#entry conditions
def E(prices, indicators, tail):
    ema25 = indicators["ema25"]
    ema50 = indicators["ema50"]
    ema100 = indicators["ema100"]
    #check for the EMA conditions

    #emas alignment
    cond1 = False
    if np.alltrue(ema25.head(tail) > ema50.head(tail)) and
        np.alltrue(ema50.head(tail) > ema100.head(tail)):
        cond1 = True

    #candles above emas
    cond2 = False
    if np.alltrue(prices.head(tail) > ema25.head(tail)):
        cond2 = True
    
   for price in prices[:] 

    
    
    


##
#exit conditions

##

backtester = Backtester(client, df, E, X)
total_profit = backtester.backtest()

##

##
for i in range(25, 0, -1): print(i)
##
df.ema25.head(5)
##
np.alltrue(df.ema25 > df.ema50)