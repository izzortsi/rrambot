##
from binance.client import Client
from grabber import *

##

#parametros

API_KEY = "XQbT3UoAVCqSr72ivWA2gBnDHAaGuNfaYdfduBMCW3VxHol4rmOCF2w8M3vr0u37"
API_SECRET = "iJ05eftlARzIcR9CHYKU81qkM21MIgvgmk5pZNvJWYLdYUgB6cS9bRLjwqBVXrQ9"
symbol="BTCUSDT"
tframe="4h"
fromdate="5 month ago"
todate = "4 month ago"
##
client = Client(api_key=API_KEY, api_secret=API_SECRET)
grab = Grabber(client)
##

df = grab.compute_indicators(symbol=symbol, tframe=tframe, fromdate=fromdate, todate=todate)

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

    def strategy(self, time, price, I):

        t0, buy_price = self.Entry

        if (self.S and self.X(price, I)):
        #if (self.S and self.X(price, buy_price)):
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

        elif (not(self.S) and self.E(price, I)):

            self.Entry = [time, price]
            print(f"comprou a {price} em {time}")
            self.S = not(self.S)
            return
        else:
            if self.S and (price/buy_price - 1 <= -0.03):
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
        i = 0

        while (i <= dataset_size - 1):
            #print(self.S)
            action = self.strategy(dates[i], prices[i], indicators.iloc[i])

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
E = lambda p, i: True if (p <= i.loc["cinf"]) else False
X = lambda p, i: True if (p >= i.loc["csup"]) else False
#X = lambda p, bp: True if (p/bp - 1 >= 0.075) else False
##

backtester = Backtester(client, df, E, X)
total_profit = backtester.backtest()

##

##
