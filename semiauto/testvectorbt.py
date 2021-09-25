import pandas as pd
import pandas_ta as ta
import vectorbt as vbt

df = pd.DataFrame().ta.ticker("AAPL")  # requires 'yfinance' installed

# Create the "Golden Cross"
df["GC"] = df.ta.sma(50, append=True) > df.ta.sma(200, append=True)

# Create boolean Signals(TS_Entries, TS_Exits) for vectorbt
golden = df.ta.tsignals(df.GC, asbool=True, append=True)

# Sanity Check (Ensure data exists)
print(df)

# Create the Signals Portfolio
pf = vbt.Portfolio.from_signals(
    df.close,
    entries=golden.TS_Entries,
    exits=golden.TS_Exits,
    freq="D",
    init_cash=100_000,
    fees=0.0025,
    slippage=0.0025,
)

# Print Portfolio Stats and Return Stats
print(pf.stats())


# %%


print(pf.returns_stats())
