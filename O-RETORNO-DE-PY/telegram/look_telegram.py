import pandas as pd
import pandas_ta as ta
from binance.client import Client
from binance.enums import *
##
from bokeh.io import output_file, show
from bokeh.models import *
from bokeh.plotting import figure
from bokeh.layouts import gridplot, column
##
from typing import Union, Callable

numeric = Union[int, float]
##

client = Client()
symbol, tframe, fromdate, todate = "BTCUSDT", "30m", "3 day ago", None
klines = client.get_historical_klines(symbol, tframe, fromdate)
replaced_fromdate = fromdate.replace(" ", "-")
output_file(f"{symbol}_{tframe}_{replaced_fromdate}.html")

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
hlc = ohlc.drop(columns=["open"])
c = ohlcv.pop("close")
h = ohlcv.pop("high")
l = ohlcv.pop("low")
v = ohlcv.pop("volume")
##
cs = ta.vwma(h, v, length=3)
cs.rename("csup", inplace=True)

cm = ta.vwma(c, v, length=3)
cm.rename("cmed", inplace=True)

ci = ta.vwma(l, v, length=3)
ci.rename("cinf", inplace=True)
##
df = pd.concat([cs, ci, c, cm, v], axis=1)
##
def look(df):
    source = ColumnDataSource(data=df)
    TOOLS = "crosshair, pan, wheel_zoom, box_zoom, reset, box_select, lasso_select"
    
    hover = HoverTool(
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
        mode='vline', line_policy='nearest', names=['cprices']
    )


    fig = figure(x_axis_type="datetime", title=f'{symbol}, {tframe}, {fromdate}',
                plot_width=950, plot_height=600,
                tools=['crosshair', 'pan', 'box_zoom', 'wheel_zoom', 'save', 'reset', hover],
                x_range=(c.index[40], c.index[80])
                )

    cline = fig.line('date', 'close', source= source, color='black', name='cprices')
    csline = fig.line('date', 'csup', source= source, color='green', line_alpha=0.8, line_dash = "dashed", name='cs')
    cmline = fig.line('date', 'cmed', source= source, color='blue', line_alpha=0.8, line_dash = "dashed", name='cm')
    ciline = fig.line('date', 'cinf', source= source, color='red', line_alpha=0.8, line_dash = "dashed", name='ci')
    
    select = figure(title="Drag the middle and edges of the selection box to change the range above",
                    plot_height=130, plot_width=800, y_range=fig.y_range,
                    x_axis_type="datetime", y_axis_type=None,
                    tools="", toolbar_location=None, background_fill_color="#efefef")
    
    c.index[0]
    
    range_tool = RangeTool(x_range=fig.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    select.line('date', 'close', source=source)
    select.line('date', 'csup', source=source)
    select.line('date', 'cmed', source=source)
    select.line('date', 'cinf', source=source)
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)
    select.toolbar.active_multi = range_tool

    return fig, select
##
fig, select = look(df)
show(column(fig, select))