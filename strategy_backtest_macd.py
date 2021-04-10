##
from binance.client import Client
from grabber import *
import numpy as np
##

#parametros

API_KEY = ""
API_SECRET = ""
symbol="BTCUSDT"
tframe="30m"
fromdate="15 day ago"
todate = None
##

##
##
replaced_fromdate = fromdate.replace(" ", "-")
nowdate = lambda: "Now" if todate == None else todate.replace(" ", "-")

##
filename = f"{symbol}_{tframe}_from={replaced_fromdate}_to={nowdate()}.txt"
##
filename
##
class GrabberMACD(Grabber):

    def compute_indicators(self, symbol="BTCUSDT", tframe="30m", fromdate="1 day ago", todate = None, indicators=[]):

        klines = self.get_data(symbol=symbol, tframe=tframe, fromdate=fromdate, todate=todate)
        ohlcv = self.trim_data(klines)

        c = ohlcv.pop("close")
        h = ohlcv.pop("high")
        l = ohlcv.pop("low")
        v = ohlcv.pop("volume")

        macd = ta.macd(c)
        macd.rename(columns={"MACD_12_26_9": "macd",
        "MACDh_12_26_9": "histogram",
        "MACDs_12_26_9": "signal"},
        inplace=True)

        df = pd.concat([c, macd], axis=1)

        return df
    

##
client = Client(api_key=API_KEY, api_secret=API_SECRET)
grab = GrabberMACD(client)
##

df = grab.compute_indicators(symbol=symbol, tframe=tframe, fromdate=fromdate, todate=todate)

##
class Backtester:

    def __init__(self, client, df, E, X, stoploss_check, period):
        self.log = []
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
        self.opscount = 0

    def strategy(self, i, dates, prices, indicators):

        price = prices.iloc[i]
        time = dates[i]
        t0, buy_price = self.Entry

        #if (self.S and self.X(price, I)):
        if (self.S and self.X(i, self.stoploss, buy_price, prices, indicators, self.period)):
            #ordem de venda
            #aqui vai ser order = ...
            #e if (order["status"] == "FILLED") return (order["orderId"], order["transactTime"], order["price"])
            #else tem que ver issae
            sell_price = float(price)
            eXit = [time, sell_price]
            profit = (sell_price - buy_price)
            percentual_profit = ((sell_price - buy_price)/buy_price)*100
            self.profits.append(percentual_profit)
            res_time = str(time - t0)
            print(f"vendeu a {sell_price} em {time}. Diferença absoluta de: {profit}; Diferença percentual: {percentual_profit}%. Tempo de resolução: {res_time} ")
            #self.log.write(f"({self.opscount}) vendeu a {sell_price} em {time}. Diferença absoluta de: {profit}; Diferença percentual: {percentual_profit}%. Tempo de resolução: {res_time}.\n")
            self.log[self.opscount].append(f"({self.opscount}) vendeu a {sell_price} em {time}. Diferença absoluta de: {profit}; Diferença percentual: {percentual_profit}%. Tempo de resolução: {res_time}.\n")
            self.opscount += 1
            self.S = not(self.S)

            return self.Entry, self.eXit, profit, res_time, self.S #tem que ver melhor que que precisa retornar

        elif (not(self.S) and self.E(i, prices, indicators, self.period)):

            self.Entry = [time, price]
            #self.stoploss = price - indicators.ema50.iloc[i]
            #print("Stoploss: ", self.stoploss)
            print(f"comprou a {price} em {time}")
            #self.log.write(f"({self.opscount}) comprou a {price} em {time}.\n")
            self.log.append([f"({self.opscount}) comprou a {price} em {time}.\n"])
            self.S = not(self.S)

            return None

        else:
            if self.S and self.stoploss_check(i, self.stoploss, buy_price, prices, indicators):
                sell_price = float(price)
                eXit = [time, sell_price]
                profit = (sell_price - buy_price)
                percentual_profit = ((sell_price - buy_price)/buy_price)*100
                self.profits.append(percentual_profit)
                res_time = str(time - t0)
                print(f"Stop-loss: vendeu a {sell_price} em {time}. Diferença absoluta de: {profit}; Diferença percentual: {percentual_profit}%. Tempo de resolução: {res_time} ")
                #self.log.write(f"({self.opscount}) STOP-LOSS: Vendeu a {sell_price} em {time}. Diferença absoluta de: {profit}; Diferença percentual: {percentual_profit}%. Tempo de resolução: {res_time}.\n")
                self.log[self.opscount].append(f"({self.opscount}) STOP-LOSS: Vendeu a {sell_price} em {time}. Diferença absoluta de: {profit}; Diferença percentual: {percentual_profit}%. Tempo de resolução: {res_time}.\n")
                self.opscount += 1
                self.S = not(self.S)
                return self.Entry, self.eXit, profit, res_time, self.S

    def backtest(self):

        prices = self.df["close"]
        indicators = self.df.loc[:, self.df.columns != "close"]
        dates = prices.index

        dataset_size = len(dates)
        i = 26 + self.period #26 é o maior número de Nans nas dataframes

        while (i <= dataset_size - 1):
            #print(self.S)
            action = self.strategy(i, dates, prices, indicators)

            if action != None:
                self.Ops.append(action[:-1])

            i += 1

        total_profit = 0
        for profit in self.profits:
            
            total_profit += profit

        #info = client.get_ticker(symbol=symbol)
        #ethprice = float(info["lastPrice"])
        print(f"Lucro percentual aproximado: {total_profit}")
        with open(f"{filename}", "w") as log:
            for i, trade in enumerate(self.log):
                #log.write(f"(({i}))\n")
                log.writelines(trade)
                #log.write(trade[1]+"\n")
            #log.write("\n")
        log = open(f"{filename}", "a")
        log.write(f"Lucro percentual total: {total_profit}%.")
        log.close()            
        #self.log.write(f"Lucro percentual total: {total_profit}")
        #self.log.close()
        return total_profit


##
#entry conditions
def E(i, prices, indicators, period):
    macd = indicators["macd"]
    histogram = indicators["histogram"]
    signal = indicators["signal"]

    if np.alltrue(histogram.iloc[:i].tail(period) < 0):
        return True
    else:
        return False
    

def stoploss_check(i, stoploss, buy_price, prices, indicators):
    return ((prices.iloc[i]/buy_price - 1)*100 <= -1.0)

def X(i, stoploss, buy_price, prices, indicators, period):
    
    macd = indicators["macd"]
    histogram = indicators["histogram"]
    signal = indicators["signal"]

    if (
        ((prices.iloc[i]/buy_price - 1)*100 >= 2.5) and #pelo menos 2.5% de lucro
        (np.alltrue(histogram.iloc[:i].tail(period) > 0))
        ):
        return True
    else:
        return False
    
    
    


##
#exit conditions

##

backtester = Backtester(client, df, E, X, stoploss_check, 6)
total_profit = backtester.backtest()


##

##
