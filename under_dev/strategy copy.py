##
from matplotlib import pyplot
import pandas as pd
import pandas_ta as ta

##


##
class Strategy:
    def __init__(self, data, entry_conditions, exit_conditions, stoploss_conditions):

        #ta_strategy fornece os indicadores e respectivos parametros

        #\*_conditions tem que ser algum conjunto de regras, bem formatado, com o qual
        #seja possível definir funçoes pra entrar, sair e stoploss
        #evidentemente, essas condições tem que ser mais fácil de escrever do que
        #simplesmente escrever as funçoes. esse é o desafio
        self.ta_strategy = ta_strategy
        self.entry_conditions = entry_conditions
        self.exit_conditions = exit_conditions
        self.stoploss_conditions = stoploss_conditions

    def E(self):
        raise NotImplementedError

    def X(self):
        raise NotImplementedError
    
    def stoploss_check(self):
        raise NotImplementedError
##
#entry conditions
def E(i, prices, indicators, period):
    
    histogram = indicators["histogram"]

    if np.alltrue(histogram.iloc[:i].tail(period) < 0):
        return True
    else:
        return False
    
#stoploss conditions
def stoploss_check(i, stoploss, buy_price, prices, indicators):
    global stoploss_parameter
    return ((prices.iloc[i]/buy_price - 1)*100 <= stoploss_parameter)

#exit conditions
def X(i, stoploss, buy_price, prices, indicators, period):

    histogram = indicators["histogram"]
    
    global take_profit
    if (
        ((prices.iloc[i]/buy_price - 1)*100 >= take_profit) and #pelo menos `take_profit` de lucro
        (np.alltrue(histogram.iloc[:i].tail(period) > 0))
        ):
        return True
    else:
        return False
##
