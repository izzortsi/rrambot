# %%

import numpy as np
import pandas as pd
import pandas_ta as ta
from binance.client import Client

from bokeh.io import output_file, show

# from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter, Cross, RangeTool
from bokeh.models import *
from bokeh.plotting import figure
from bokeh.layouts import gridplot, column, grid, row
from new_srcs.grabber import DataGrabber
from new_srcs.bokeh_dashboard import *

# %%


data_params_30m = {"symbol": "BNBUSDT", "timeframe": "30m", "fromdate": "7 day ago"}
db30m = Dashboard(data_params_30m)
figs_30m = db30m.bokeh_plot()
# %%
data_params_4h = {"symbol": "BNBUSDT", "timeframe": "4h", "fromdate": "56 day ago"}
db4h = Dashboard(data_params_4h)
figs_4h = db4h.bokeh_plot()

# %%
show(gridplot([column(*figs_30m), column(*figs_4h)], ncols=2))
