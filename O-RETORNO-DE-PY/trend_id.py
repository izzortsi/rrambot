#%%

def trend_test(tail: int, ema25, ema50, ema100, ohlcv) -> bool:

    i, b = 0, True

    while i < tail:
    
        if not b: 
            break
        
        if np.alltrue(ema25 > ema50) and 
            np.alltrue(ema50 > ema100) and 
            np.alltrue(ohlcv["low"] > ema25):
                None
        else:
            b = False
    
    return b

# %%

# %%
!True
# %%
b = True;
not b
# %%
