# %%

import numpy as np
import pandas as pd
import pandas_ta as ta
from binance.client import Client
from binance.helpers import *

from bokeh.io import output_file, show

# from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter, Cross, RangeTool
from bokeh.models import *
from bokeh.plotting import figure
from bokeh.layouts import gridplot, column, grid, row
from new_srcs.grabber import DataGrabber
from new_srcs.bokeh_dashboard import *

# %%
symbol = "COTIUSDT"
timeframes = ["1h", "4h"]
# %%
def interval_to_sec(interval: str):
    seconds_per_unit: Dict[str, int] = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60,
        }
    try:
        return int(interval[:-1]) * seconds_per_unit[interval[-1]]
    except (ValueError, KeyError):
        return None
# %%
def sync_intervals(time_range: str, interval_1: str, interval_2: str):
    trange_unit = time_range[-1]
    trange_sec = interval_to_sec(time_range)
    i1_sec = interval_to_sec(interval_1)
    i2_sec = interval_to_sec(interval_2)
    assert i1_sec <= i2_sec
    n_units = int((trange_sec/i1_sec)*i2_sec/interval_to_sec(f"1{trange_unit}"))
    return f"{n_units}{trange_unit}"


# %%
sync_intervals("10d", "30m", "4h")
# %%

# %%

 

 

data_params_30m = {
    "symbol": symbol,
    "timeframe": timeframes[0],
    "fromdate": "7 day ago",
}
db30m = Dashboard(data_params_30m)
figs_30m = db30m.bokeh_plot()
# %%
data_params_4h = {
    "symbol": symbol,
    "timeframe": timeframes[1],
    "fromdate": "56 day ago",
}
db4h = Dashboard(data_params_4h)
figs_4h = db4h.bokeh_plot()

# %%
show(gridplot([column(*figs_30m), column(*figs_4h)], ncols=2))
