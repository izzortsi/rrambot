from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.stats
import pandas as pd

# escrever as funcoes pra calcular os indicadores,
# preocupar-se com a interface... nao precisa fazer quase nada, usando o pandas_ta
##
import pandas as pd
import pandas_ta
from pandas_ta import *

# %%


def vwema(close, volume, length=None, offset=None, **kwargs):
    """Indicator: Volume Weighted Moving Average (VWMA)"""
    # Validate Arguments
    length = int(length) if length and length > 0 else 10
    close = verify_series(close, length)
    volume = verify_series(volume, length)
    offset = get_offset(offset)

    if close is None or volume is None:
        return

    # Calculate Result
    pv = close * volume
    vwema = ema(close=pv, length=length) / ema(close=volume, length=length)

    # Offset
    if offset != 0:
        vwema = vwema.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        vwema.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        vwema.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    vwema.name = f"VWEMA_{length}"
    vwema.category = "overlap"

    return vwema


vwema.__doc__ = """Volume Weighted Exponential Moving Average (VWEMA)

Volume Weighted Exponential Moving Average.

Sources:
    ##

Calculation:
    Default Inputs:
        length=10
    EMA = Simple Moving Average
    pv = close * volume
    VWEMA = EMA(pv, length) / EMA(volume, length)

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    length (int): It's period. Default: 10
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""

pandas_ta.vwema = vwema
