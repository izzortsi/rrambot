# %%


from tradingview_ta import *
from symbols_formats import FORMATS

# %%
symbols = FORMATS.keys()
symbols = list(symbols)
tv_symbols = symbols.copy()

for i, symbol in enumerate(tv_symbols):
    tv_symbols[i] = "BINANCE:" + symbol

# %%

tv_symbols[1]
# %%
analysis = get_multiple_analysis(
    screener="crypto",
    interval="1m",
    symbols=tv_symbols,
)

# %%


handler = TA_Handler(
    symbol="BNBUSDTPERP",
    exchange="binance",
    screener="crypto",
    interval="15m",
    timeout=None,
)


# %%

handler.get_analysis().summary

# %%

analysis["BINANCE:COTIUSDT"].interval
analysis["BINANCE:COTIUSDT"].summary
# %%
from binance.helpers import *
 
# %%
