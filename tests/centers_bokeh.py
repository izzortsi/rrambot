# %%


import pandas as pd
import pandas_ta as ta
from binance.client import Client

from bokeh.io import output_file, show

# from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter, Cross, RangeTool
from bokeh.models import *
from bokeh.plotting import figure
from bokeh.layouts import gridplot, column

# %%


client = Client()

symbol, tframe, fromdate = "XLMUSDT", "1h", "60 day ago"
N = 3


def get_data(symbol, tframe, fromdate):
    klines = client.get_historical_klines(symbol, tframe, fromdate)
    replaced_fromdate = fromdate.replace(" ", "-")
    return trim_data(klines)


def trim_data(rdata):
    df = pd.DataFrame(data=rdata)
    DOHLCV = df.iloc[:, [0, 1, 2, 3, 4, 5]]
    DOHLCV[0] = pd.to_datetime(DOHLCV[0], unit="ms")
    DOHLCV.columns = ["date", "open", "high", "low", "close", "volume"]
    DOHLCV.ta.adjusted = "adj_close"
    OHLCV = DOHLCV.iloc[:, [1, 2, 3, 4, 5]]
    OHLCV.set_index(pd.DatetimeIndex(DOHLCV["date"]), inplace=True)
    OHLCV = OHLCV.astype("float64")
    return OHLCV


ta.vwma()

Indicators = ta.Strategy(
    name="EMAs, BBs, and MACD",
    description="Non Multiprocessing Strategy by rename Columns?",
    ta=[
        {"kind": "ema", "length": 8},
        {"kind": "ema", "length": 21},
        {"kind": "bbands", "length": 20, "col_names": ("BBL", "BBM", "BBU")},
        {
            "kind": "macd",
            "fast": 8,
            "slow": 21,
            "col_names": ("MACD", "MACD_H", "MACD_S"),
        },
    ],
)
# Run it
df.ta.strategy(NonMPStrategy)

# %%
output_file(f"{symbol}_{tframe}_{replaced_fromdate}.html")


# %%
ohlcv = get_data(symbol, tframe, fromdate)
c = ohlcv["close"]
h = ohlcv["high"]
l = ohlcv["low"]
v = ohlcv["volume"]
# %%
ta.mom(v, length=4)
# %%
# ohlcv.ta.adjusted = "adj_close"

# df.ta.adjusted = None
# ohlc = ohlcv.drop(columns=["volume"])
# hlc = ohlc.drop(columns=["open"])

# %%


cs = ta.vwma(h, v, length=N)
cs.rename("csup", inplace=True)

cm = ta.vwma(c, v, length=N)
cm.rename("cmed", inplace=True)

ci = ta.vwma(l, v, length=3)
ci.rename("cinf", inplace=True)
# %%


# roc = ta.roc(c, length=5)
rsi = ta.rsi(c, length=7)
# %%
# rsi_mean = rsi.mean()
# rsi_std = rsi.std()
# rsi = (rsi - rsi_mean)/rsi_std
# %%


# %%
macd = ta.macd(c)
macd_h = macd["MACDh_12_26_9"]
# %%
macd_mean = macd.mean()
macd_std = macd.std()

macd = (macd - macd_mean) / macd_std
macd
# %%
macd_h = macd["MACDh_12_26_9"]
# hstd = macd_h.std()
# hmean = macd_h.mean()
# nmacd_h = (macd_h - hmean) / hstd
# %%
D1h = macd_h.shift(1) - macd_h
# D1h = (D1h - D1h.mean()) / D1h.std()
D1h = D1h.rename("D1h")
D2h = D1h.shift(1) - D1h
# D2h = (D2h - D2h.mean()) / D2h.std()
D2h = D2h.rename("D2h")

# %%
df = pd.concat([cs, ci, c, cm, v, macd, rsi, D1h, D2h], axis=1)
# df.ta.adjusted = "adj_close"
# %%


class BokehFigure:

    source = ColumnDataSource(data=df)
    # TOOLS = "crosshair, pan, wheel_zoom, box_zoom, reset, box_select, lasso_select"
    hover = HoverTool(
        tooltips=[
            ("time", "@date{%m/%d %H:%M}"),
            ("close", "$@{close}{%0.2f}"),  # use @{ } for field names with spaces
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

    # %%

    cylims = (min(df.cinf), max(df.csup))
    fig = figure(
        x_axis_type="datetime",
        title=f"{symbol}, {tframe}, {fromdate}",
        plot_width=950,
        plot_height=250,
        tools=["crosshair", "pan", "box_zoom", "wheel_zoom", "save", "reset", hover],
        active_scroll="wheel_zoom",
        x_range=(c.index[40], c.index[80]),
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
        plot_height=130,
        plot_width=800,
        y_range=fig.y_range,
        x_axis_type="datetime",
        y_axis_type=None,
        tools="",
        toolbar_location=None,
        background_fill_color="#efefef",
    )
    # %%

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
    # %%

    macd_hover = HoverTool(
        tooltips=[
            ("time", "@date{%m/%d %H:%M}"),
            ("close", "$@{close}{%0.2f}"),  # use @{ } for field names with spaces
            ("histogram", "@MACDh_12_26_9"),
        ],
        formatters={
            "@date": "datetime",  # use 'datetime' formatter for '@date' field
            "@{close}": "printf",  # use 'printf' formatter for '@{adj close}' field
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
            ("close", "$@{close}{%0.2f}"),  # use @{ } for field names with spaces
            ("D1h", "@D1h"),
        ],
        formatters={
            "@date": "datetime",  # use 'datetime' formatter for '@date' field
            "@{close}": "printf",  # use 'printf' formatter for '@{adj close}' field
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
            ("close", "$@{close}{%0.2f}"),  # use @{ } for field names with spaces
            ("D2h", "@D2h"),
        ],
        formatters={
            "@date": "datetime",  # use 'datetime' formatter for '@date' field
            "@{close}": "printf",  # use 'printf' formatter for '@{adj close}' field
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
            ("close", "$@{close}{%0.2f}"),  # use @{ } for field names with spaces
            ("rsi7", "@RSI_7"),
        ],
        formatters={
            "@date": "datetime",  # use 'datetime' formatter for '@date' field
            "@{close}": "printf",  # use 'printf' formatter for '@{adj close}' field
            # use default 'numeral' formatter for other fields
        },
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode="vline",
        line_policy="nearest",
        names=["rsi_line"],
    )

    # %%
    macd_fig = figure(
        x_axis_type="datetime",
        title=f"{symbol}, {tframe}, MACDH",
        plot_width=950,
        plot_height=250,
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
        title=f"{symbol}, {tframe}, RSI7",
        plot_width=950,
        plot_height=250,
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
    # %%
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
        title=f"{symbol}, {tframe}, D1h",
        plot_width=950,
        plot_height=200,
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
        title=f"{symbol}, {tframe}, MACDh derivatives",
        plot_width=950,
        plot_height=200,
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
    # %%
    show(
        column(
            fig,
            macd_fig,
            D1h_fig,
            D2h_fig,
            rsi_fig,
            select,
            sizing_mode="stretch_height",
        )
    )


# %%
plots = gridplot([[plot1], [plot2]], sizing_mode="scale_width")
