import time
from binance import ThreadedWebsocketManager

api_key = "tF8GCAOYQ6G8fqgiwPDv3cDGfPOJffrXpYUcgkcEY38UCTRxG8D7fblZwyOFoMEA"
api_secret = "J4Gp5w0jdg2LICtXt1yY41TXWTOyrWCifCSMdyGtfMgVMVNFVDClnSXV9Tvh7zRT"


# %%

class Manager:
    def __init__(self, api_key, api_secret):
        self.data = {}
        self.twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
        # start is required to initialise its internal loop
        self.twm.start()

    def start_stream(self, symbol="BNBUSDT"):
        stream_name = self.twm.start_kline_socket(callback=self.handle_socket_message, symbol=symbol)
        return stream_name

    def handle_socket_message(self, msg):
        print(f"message type: {msg['e']}")
        print(f"message type: {msg['k']['c']}")
        self.data[f"{msg['k']['s']}_{msg['k']['i']}"]=msg['k']['c']

# %%
manager = Manager(api_key, api_secret)

# %%
stream1 = manager.start_stream()
stream2 = manager.start_stream(symbol="BTCUSDT")

# %%
manager.data
# %%
manager.twm.stop_socket(stream1)
manager.twm.stop_socket(stream2)
