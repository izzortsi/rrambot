import tradingview_ta as tv

tv.TA_Handler.indicators = tv.TA_Handler.indicators + ["high", "low", "close", "change"]
# %%
# %%
symbol = "ADAUSDT"
tfs = ["5m", "1h", "1d"]
# %%
def make_handlers(tfs=["5m", "1h", "1d"], symbol="ADAUSDT"):
    def tah(symbol, interval):
        H = tv.TA_Handler(
            symbol=symbol,
            exchange="binance",
            screener="crypto",
            interval=interval,
            timeout=None,
        )
        H.indicators + ["high", "low", "close", "change"]
        return H

    handlers = {symbol: {tf: tah(symbol, tf) for tf in tfs}}
    return handlers


h = make_handlers()


def indicators(tfs, symbol, handlers):
    indicators = {symbol: {tf: None for tf in tfs}}
    for tf in tfs:
        h_ind = handlers[symbol][tf].get_indicators()
        h_ind["MACD.histogram"] = h_ind["MACD.macd"] - h_ind["MACD.signal"]
        h_ind["MACD.histogram"] = h_ind["MACD.macd"] - h_ind["MACD.signal"]
        indicators[symbol][tf] = h_ind
    return indicators


# %%
indicators = indicators(tfs, symbol, h)
# %%
indicators

# %%
ind15m

# %%
ind1h
# %%

# %%
ind1d


def macd_hist(ind):
    ind["MACD.histogram"] = ind["MACD.macd"] - ind["MACD.signal"]


macd_hist(ind1d)

ind1d["MACD.histogram"]
ind1
# %%

# %%
