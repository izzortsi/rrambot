# %%

import numpy as np
import pandas as pd
import pandas_ta as ta
from binance.client import Client

from bokeh.io import output_file, show

# from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter, Cross, RangeTool
from bokeh.models import *
from bokeh.plotting import figure
from bokeh.layouts import gridplot, column
from plots.grabber import DataGrabber


# %%
global N
N = 5
# %%
client = Client()
# symbol, timeframe, fromdate = "BNBUSDT", "15m", "4 day ago"
data_params = {"symbol": "BNBUSDT", "timeframe": "30m", "fromdate": "6 day ago"}
symbol, timeframe, fromdate = data_params.values()

dg = DataGrabber(client)
ohlcv = dg.get_data(**data_params)
df = dg.compute_indicators(ohlcv)
df.dropna(how="any", inplace=True)
# %%

replaced_fromdate = fromdate.replace(" ", "-")
output_file(f"{symbol}_{timeframe}_{replaced_fromdate}.html")


def bokeh_plot(
    df,
    show_plot=False,
    **data_params,
):
    symbol, timeframe, fromdate = data_params.values()
    source = ColumnDataSource(data=df)
    TOOLS = "crosshair, pan, wheel_zoom, box_zoom, reset, box_select, lasso_select"
    data_length = len(df)
    hover = HoverTool(
        tooltips=[
            ("time", "@date{%m/%d %H:%M}"),
            ("close", "$@{close}{%0.4f}"),  # use @{ } for field names with spaces
            ("volume", "@volume{0.00 a}"),
        ],
        formatters={
            "@date": "datetime",  # use 'datetime' formatter for '@date' field
            "@{close}": "printf",  # use 'printf' formatter for '@{adj close}' field
            # use default 'numeral' formatter for other fields
        },
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode="vline",
        line_policy="nearest",
        names=["cprices"],
    )
    cylims = (min(df.cinf), max(df.csup))
    fig = figure(
        x_axis_type="datetime",
        title=f"{symbol}, {timeframe}, {fromdate}",
        plot_width=600,
        plot_height=200,
        tools=["crosshair", "pan", "box_zoom", "wheel_zoom", "save", "reset", hover],
        x_range=(
            df.index[data_length // 5],
            df.index[3 * data_length // 5],
        ),
        active_scroll="wheel_zoom",
        y_range=cylims,
    )

    cline = fig.line("date", "close", source=source, color="black", name="cprices")

    csline = fig.line(
        "date",
        "csup",
        source=source,
        color="green",
        line_alpha=0.8,
        line_dash="dashed",
        name="cs",
    )
    cmline = fig.line(
        "date",
        "cmed",
        source=source,
        color="blue",
        line_alpha=0.8,
        line_dash="dashed",
        name="cm",
    )
    ciline = fig.line(
        "date",
        "cinf",
        source=source,
        color="red",
        line_alpha=0.8,
        line_dash="dashed",
        name="ci",
    )

    select = figure(
        title="Drag the middle and edges of the selection box to change the range above",
        plot_height=100,
        plot_width=600,
        y_range=fig.y_range,
        x_axis_type="datetime",
        y_axis_type=None,
        tools="",
        toolbar_location=None,
        background_fill_color="#efefef",
    )

    range_tool = RangeTool(x_range=fig.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    select.line("date", "close", source=source)
    select.line("date", "csup", source=source)
    select.line("date", "cmed", source=source)
    select.line("date", "cinf", source=source)
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)
    select.toolbar.active_multi = range_tool

    macd_hover = HoverTool(
        tooltips=[
            ("time", "@date{%m/%d %H:%M}"),  # use @{ } for field names with spaces
            ("histogram", "@MACDh_12_26_9"),
        ],
        formatters={
            "@date": "datetime",  # use 'datetime' formatter for '@date' field
            # use default 'numeral' formatter for other fields
        },
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode="vline",
        line_policy="nearest",
        names=["hist_line"],
    )
    d1h_hover = HoverTool(
        tooltips=[
            ("time", "@date{%m/%d %H:%M}"),
            ("D1h", "@D1h"),
        ],
        formatters={
            "@date": "datetime",  # use 'datetime' formatter for '@date' field
            # use default 'numeral' formatter for other fields
        },
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode="vline",
        line_policy="nearest",
        names=["D1h_line"],
    )
    d2h_hover = HoverTool(
        tooltips=[
            ("time", "@date{%m/%d %H:%M}"),
            ("D2h", "@D2h"),
        ],
        formatters={
            "@date": "datetime",  # use 'datetime' formatter for '@date' field
            # use default 'numeral' formatter for other fields
        },
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode="vline",
        line_policy="nearest",
        names=["D2h_line"],
    )
    rsi_hover = HoverTool(
        tooltips=[
            ("time", "@date{%m/%d %H:%M}"),
            ("rsi7", "@RSI_7"),
        ],
        formatters={
            "@date": "datetime",  # use 'datetime' formatter for '@date' field
            # use default 'numeral' formatter for other fields
        },
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode="vline",
        line_policy="nearest",
        names=["rsi_line"],
    )

    macd_fig = figure(
        x_axis_type="datetime",
        title=f"{symbol}, {timeframe}, MACDH",
        plot_width=600,
        plot_height=150,
        tools=[
            "crosshair",
            "pan",
            "box_zoom",
            "wheel_zoom",
            "save",
            "reset",
            macd_hover,
        ],
        active_scroll="wheel_zoom",
        x_range=fig.x_range,
    )
    rsi_fig = figure(
        x_axis_type="datetime",
        title=f"{symbol}, {timeframe}, RSI7",
        plot_width=600,
        plot_height=150,
        tools=[
            "crosshair",
            "pan",
            "box_zoom",
            "wheel_zoom",
            "save",
            "reset",
            rsi_hover,
        ],
        active_scroll="wheel_zoom",
        x_range=fig.x_range,
    )

    hist_line = macd_fig.line(
        "date",
        "MACDh_12_26_9",
        source=source,
        color="green",
        line_alpha=1.0,
        line_dash="dashed",
        name="hist_line",
    )
    macd_line = macd_fig.line(
        "date",
        "MACD_12_26_9",
        source=source,
        color="red",
        line_alpha=0.8,
        name="macd_line",
    )
    signal_line = macd_fig.line(
        "date",
        "MACDs_12_26_9",
        source=source,
        color="blue",
        line_alpha=0.8,
        name="signal_line",
    )
    rsi_line = rsi_fig.line(
        "date",
        "RSI_7",
        source=source,
        color="green",
        line_alpha=1.0,
        name="rsi_line",
    )

    D1h_fig = figure(
        x_axis_type="datetime",
        title=f"{symbol}, {timeframe}, 1st MACDh derivative",
        plot_width=600,
        plot_height=150,
        tools=[
            "crosshair",
            "pan",
            "box_zoom",
            "wheel_zoom",
            "save",
            "reset",
            d1h_hover,
        ],
        active_scroll="wheel_zoom",
        x_range=fig.x_range,
    )
    D1h_line = D1h_fig.line(
        "date",
        "D1h",
        source=source,
        color="red",
        line_alpha=1.0,
        name="D1h_line",
    )
    D2h_fig = figure(
        x_axis_type="datetime",
        title=f"{symbol}, {timeframe}, 2nd MACDh derivative",
        plot_width=600,
        plot_height=150,
        tools=[
            "crosshair",
            "pan",
            "box_zoom",
            "wheel_zoom",
            "save",
            "reset",
            d2h_hover,
        ],
        active_scroll="wheel_zoom",
        x_range=fig.x_range,
    )
    D2h_line = D2h_fig.line(
        "date",
        "D2h",
        source=source,
        color="blue",
        line_alpha=1.0,
        name="D2h_line",
    )

    figs = [fig, macd_fig, D1h_fig, D2h_fig, rsi_fig, select]

    def link_crosshairs(figs):
        crosshair = CrosshairTool(dimensions="both")
        for fig in figs:
            fig.add_tools(crosshair)

    link_crosshairs(figs)

    if show_plot:
        p = column(*figs)
        show(p)
    return figs


# %%
figs = bokeh_plot(df, **data_params, show_plot=False)
# %%
show(column(*figs))
# %%
