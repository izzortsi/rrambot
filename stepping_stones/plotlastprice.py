import unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager as ubwam
import datetime as dt
from matplotlib import use
import matplotlib.pyplot as plt
import matplotlib.animation as animation

print("Please install `matplotlib`! https://pypi.org/project/matplotlib")


matplotlib.use('qt5agg')
# %%
%matplotlib

# %%

binance_websocket_api_manager = ubwam.BinanceWebSocketApiManager()
binance_websocket_api_manager.create_stream("trade", "btcusdt", output="UnicornFy")

xs = []
ys = []
title = "Live BTC Price @ Binance.com"
fig = plt.figure()
fig.canvas.set_window_title(title)
ax = fig.add_subplot(1, 1, 1)

print("Please wait a few seconds until enough data has been received!")

# %%
def animate(i, xs, ys):
    data = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
    try:
        if data["stream_type"]:
            xs.append(dt.datetime.fromtimestamp(data["trade_time"] / 1000))
            ys.append(float(data["price"]))
            ax.clear()
            ax.plot(xs, ys)
            plt.xticks(rotation=45, ha="right")
            plt.subplots_adjust(bottom=0.30)
            plt.title(title)
            plt.ylabel("USDT Value")
    except KeyError:
        pass
    except TypeError:
        pass


# %%

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=5)
plt.show()
