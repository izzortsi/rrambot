from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor


class Manager:
    def __init__(self, api_key=None, api_secret=None):
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self.bsm = BinanceSocketManager(self.client)
        self.traders = {}
        self.trading = []

    def add_trader(self, strategy, init_val, symbol, timeframe):

        name = f"{symbol}_{timeframe}_{strategy.name}"
        atrader = ATrader(name, self, strategy, init_val, symbol, timeframe)
        self.traders[name] = atrader

    def process_message(self, msg):
        """ define how to process incoming WebSocket messages """
        if msg["e"] != "error":
            print(msg["k"]["c"])
            self.exitprices.append(msg["k"]["c"])
            self.lastcandles.append(msg["k"])
        else:
            self.socket_error = True

    def remove_trader(self, name=None, conditions=None):
        # remove um trader diretamente pelo nome ou por condiçoes (como determiná-las?)
        raise NotImplementedError

    def get_traders(self):
        print(self.traders.keys)
        return self.traders
