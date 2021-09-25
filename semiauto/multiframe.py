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

# from new_srcs.grabber import DataGrabber
# from new_srcs.bokeh_dashboard import *
from semiauto.grabber import DataGrabber
from semiauto.auxs_functions import *
from semiauto.bokeh_chart import GridChart

# %%
symbol = "COTIUSDT"
timeframes = ["1h", "4h"]
# %%


# %%
sync_intervals("10d", "30m", "4h")
# %%

# %%


data_params_30m = {
    "symbol": symbol,
    "timeframe": timeframes[0],
    "fromdate": "7 day ago",
}
db30m = GridChart(data_params_30m)
figs_30m = db30m.bokeh_plot()
db30m.df[list(("MACD_12_26_9", "MACDh_12_26_9", "MACDs_12_26_9"))].max().max()
db30m.df[list(("D1h",))].max().max()
# %%
data_params_4h = {
    "symbol": symbol,
    "timeframe": timeframes[1],
    "fromdate": "56 day ago",
}
db4h = GridChart(data_params_4h)
figs_4h = db4h.bokeh_plot()

# %%
show(gridplot([column(*figs_30m), column(*figs_4h)], ncols=2))

# %%
