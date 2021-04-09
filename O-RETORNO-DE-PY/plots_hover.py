
#%%
import pandas as pd
import pandas_ta as ta
from binance.client import Client
#from bokeh.io import output_file, show
#from bokeh.models import ColumnDataSource
#from bokeh.plotting import ColumnDataSource, figure, output_file, show
#from bokeh.models.tools import HoverTool
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter
from bokeh.plotting import figure
from bokeh.layouts import gridplot
##

#%%
output_file("brushing.html")

# Load data

client = Client()
klines = client.get_historical_klines("BTCUSDT", "30m", "1 day ago")
##
def trim_data(rdata):
    df = pd.DataFrame(data = rdata)
    DOHLCV = df.iloc[:, [0, 1, 2, 3, 4, 5]]
    DOHLCV[0] = pd.to_datetime(DOHLCV[0], unit='ms')
    DOHLCV.columns = ["date", "open", "high", "low", "close", "volume"]
    OHLCV = DOHLCV.iloc[:, [1, 2, 3, 4, 5]]
    OHLCV.set_index(pd.DatetimeIndex(DOHLCV["date"]), inplace=True)
    OHLCV = OHLCV.astype('float64')
    return OHLCV


##
ohlcv = trim_data(klines)
ohlc = ohlcv.drop(columns=["volume"])


source = ColumnDataSource(ohlcv)


TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"
##

# create a new plot and add a renderer
left = figure(x_axis_type="datetime", tools=TOOLS, plot_width=300, plot_height=300, title="closes")
left.line('date', 'close', source=source)

##

right = figure(x_axis_type="datetime", tools=TOOLS, x_range = left.x_range, plot_width=300, plot_height=300, title="volumes")
right.line('date', 'volume', source=source)

##
left.add_tools(HoverTool(
    tooltips=[
        ( 'time',   '@date{%m/%d %H:%M}'            ),
        ( 'close',  '$@{close}{%0.2f}' ), # use @{ } for field names with spaces
        ( 'volume', '@volume{0.00 a}'      ),
    ],

    formatters={
        '@date'        : 'datetime', # use 'datetime' formatter for '@date' field
        '@{close}' : 'printf',   # use 'printf' formatter for '@{adj close}' field
                                     # use default 'numeral' formatter for other fields
    },

    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
    )
)

right.add_tools(HoverTool(
    tooltips=[
        ( 'time',   '@date{%m/%d %H:%M}'            ),
        ( 'close',  '$@{close}{%0.2f}' ), # use @{ } for field names with spaces
        ( 'volume', '@volume{0.00 a}'      ),
    ],

    formatters={
        '@date'        : 'datetime', # use 'datetime' formatter for '@date' field
        '@{close}' : 'printf',   # use 'printf' formatter for '@{adj close}' field
                                     # use default 'numeral' formatter for other fields
    },

    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
    )
)
##
p = gridplot([[left, right]])

show(p)
##

##

##

##

##

##
