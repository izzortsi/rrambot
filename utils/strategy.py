class Strategy:
    def __init__(self, ta_strategy, entry_conditions, exit_conditions, stoploss_conditions):
        raise NotImplementedError
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