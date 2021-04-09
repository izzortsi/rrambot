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
fromdate="10 day ago"
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

    def __init__(self, client, df, E, X, stoploss_check, period):
        self.client = client
        self.df = df
        self.E = E
        self.X = X
        self.stoploss_check = stoploss_check
        self.S = False
        self.Ops = []
        self.profits = []
        self.Entry = [None, None]
        self.eXit = [None, None]
        self.period = period
        self.stoploss = None

    def strategy(self, i, dates, prices, indicators):

        price = prices.iloc[i]
        time = dates[i]
        t0, buy_price = self.Entry

        #if (self.S and self.X(price, I)):
        if (self.S and self.X(i, self.stoploss, buy_price, prices, indicators)):
            #ordem de venda
            #aqui vai ser order = ...
            #e if (order["status"] == "FILLED") return (order["orderId"], order["transactTime"], order["price"])
            #else tem que ver issae
            sell_price = float(price)
            eXit = [time, sell_price]
            profit = (sell_price - buy_price)
            percentual_profit = (sell_price - buy_price)/buy_price
            self.profits.append(percentual_profit)
            res_time = str(time - t0)
            print(f"vendeu a {sell_price} em {time}. Diferença de: {profit}, {percentual_profit}. Tempo de resolução: {res_time} ")
            self.S = not(self.S)

            return self.Entry, self.eXit, profit, res_time, self.S #tem que ver melhor que que precisa retornar

        elif (not(self.S) and self.E(i, prices, indicators, self.period)):

            self.Entry = [time, price]
            self.stoploss = price - indicators.ema50.iloc[i]
            print("Stoploss: ", self.stoploss)
            print(f"comprou a {price} em {time}")

            self.S = not(self.S)
            return
        else:
            if self.S and self.stoploss_check(i, self.stoploss, buy_price, prices, indicators):
                sell_price = float(price)
                eXit = [time, sell_price]
                profit = (sell_price - buy_price)
                percentual_profit = (sell_price - buy_price)/buy_price
                self.profits.append(percentual_profit)
                res_time = str(time - t0)
                print(f"Stop-loss: vendeu a {sell_price} em {time}. Diferença de: {profit}, {percentual_profit}. Tempo de resolução: {res_time} ")
                self.S = not(self.S)
                return self.Entry, self.eXit, profit, res_time, self.S

    def backtest(self):

        prices = self.df["close"]
        indicators = self.df.loc[:, self.df.columns != "close"]
        dates = prices.index

        dataset_size = len(dates)
        i = 100 + self.period

        while (i <= dataset_size - 1):
            #print(self.S)
            action = self.strategy(i, dates, prices, indicators)

            if action != None:
                self.Ops.append(action[:-1])

            i += 1

        total_profit = 0
        for profit in self.profits:
            
            total_profit += profit

        info = client.get_ticker(symbol=symbol)
        ethprice = float(info["lastPrice"])
        print(f"Lucro percentual aproximado: {total_profit}")

        return total_profit


##
#entry conditions
def E(i, prices, indicators, period):
    ema25 = indicators["ema25"]
    ema50 = indicators["ema50"]
    ema100 = indicators["ema100"]
    #check for the EMA conditions

    #emas alignment
    cond1 = False
    if (np.alltrue(ema25.iloc[:i].tail(period) > ema50.iloc[:i].tail(period)) 
    and np.alltrue(ema50.iloc[:i].tail(period) > ema100.iloc[:i].tail(period))):
        cond1 = True
    #print(cond1)
    #candles above emas
    cond2 = False
    if np.alltrue(prices.iloc[:i].tail(period) > ema25.iloc[:i].tail(period)):
        cond2 = True
    
    cond3 = False
    cond4 = False
    for (j, price) in enumerate(prices.iloc[i:]):
        #testa se caiu pra < ema25/50
        if ((price < ema25.iloc[j]) or (price < ema50.iloc[j])) and (price > ema100.iloc[j]):
            cond3 = True
        #se sim, continua até verificar ou buy signal
        if (cond3 == True) and (price > ema25.iloc[j]):
            cond4 = True
        #ou cancelar o setup
        elif (cond3 == True) and (price < ema100.iloc[j]):
            cond3 = False
    #print(cond1, cond2, cond3, cond4)
    return (cond1 and cond2 and cond3 and cond4)


def stoploss_check(i, stoploss, buy_price, prices, indicators):
    return prices.iloc[i] - buy_price <= -stoploss

def X(i, stoploss, buy_price, prices, indicators):
    if prices.iloc[i] - buy_price >= 1.5*stoploss:
        return True
    else:
        return False
    
    
    


##
#exit conditions

##

backtester = Backtester(client, df, E, X, stoploss_check, 15)
total_profit = backtester.backtest()


##
ema25 = df.ema25
ema50 = df.ema50
ema100 = df.ema100
prices = df.close
i=200
period = 25
##
dfplot = pd.concat([ema50.iloc[150:], ema100.iloc[150:], ema25.iloc[150:], df.close.iloc[150:]], axis=1)
##
dfplot

##

df.index
##
#dfplot.plot(color=["b", "r", "g", "k"])
##
import pandas_bokeh
pd.set_option('plotting.backend', 'pandas_bokeh')
pandas_bokeh.output_file("Interactive Plot.html")
##
dfplot.plot_bokeh(figsize=(1600, 1000),kind="line", colormap=["blue", "red", "green", "black"])
##
