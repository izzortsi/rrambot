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
from semiauto.grabber import DataGrabber


# %%

# data_params = {"symbol": "BNBUSDT", "timeframe": "15m", "fromdate": "6 day ago"}
# symbol, timeframe, fromdate = data_params.values()


class GridChart:
    def __init__(self, data_params):

        self.client = Client()
        self.dg = DataGrabber(self.client)

        self.ohlcv = self.dg.get_data(**data_params)

        self.df = self.dg.compute_indicators(self.ohlcv)
        self.df.dropna(how="any", inplace=True)

        self.data_params = data_params
        self.set_output_file()

    def set_output_file(self):
        symbol, timeframe, fromdate = self.data_params.values()
        replaced_fromdate = fromdate.replace(" ", "-")
        output_file(f"{symbol}_{timeframe}_{replaced_fromdate}.html")

    def bokeh_plot(self, show_plot=False):

        df = self.df
        symbol, timeframe, fromdate = self.data_params.values()
        source = ColumnDataSource(data=df)
        # TOOLS = "crosshair, pan, wheel_zoom, box_zoom, reset, box_select, lasso_select"
        TOOLS = "crosshair, xpan, xwheel_zoom, reset, save"
        data_length = len(df)
        hover = HoverTool(
            tooltips=[
                (" ", "@date{%m/%d %H:%M}"),
                ("close", "$@{close}{%0.4f}"),  # use @{ } for field names with spaces
                ("vol", "@volume{0.00 a}"),
            ],
            formatters={
                "@date": "datetime",  # use 'datetime' formatter for '@date' field
                "@{close}": "printf",  # use 'printf' formatter for '@{adj close}' field
                # use default 'numeral' formatter for other fields
            },
            # display a tooltip whenever the cursor is vertically in line with a glyph
            show_arrow=False,
            point_policy="snap_to_data",
            mode="vline",
            line_policy="nearest",
            names=["cprices"],
        )
        # cylims = (min(df.cinf), max(df.csup))
        fig = figure(
            x_axis_type="datetime",
            title=f"{symbol}, {timeframe}, {fromdate}",
            plot_width=600,
            plot_height=200,
            x_range=(
                df.index[data_length // 5],
                df.index[3 * data_length // 5],
            ),
            tools=TOOLS,
            sizing_mode="stretch_both",
            active_scroll="xwheel_zoom",
            active_drag="xpan",
            # aspect_ratio=2.2,
            # match_aspect=True,
            # height_policy="max",
            # sizing_mode="fixed",
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
            # y_range=fig.y_range,
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
            show_arrow=False,
            point_policy="snap_to_data",
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
            show_arrow=False,
            point_policy="snap_to_data",
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
            show_arrow=False,
            point_policy="snap_to_data",
            mode="vline",
            line_policy="nearest",
            names=["D2h_line"],
        )
        mfi_hover = HoverTool(
            tooltips=[
                ("time", "@date{%m/%d %H:%M}"),
                ("mfi14", "@MFI_14"),
            ],
            formatters={
                "@date": "datetime",  # use 'datetime' formatter for '@date' field
                # use default 'numeral' formatter for other fields
            },
            # display a tooltip whenever the cursor is vertically in line with a glyph
            show_arrow=False,
            point_policy="snap_to_data",
            mode="vline",
            line_policy="nearest",
            names=["mfi_line"],
        )

        macd_fig = figure(
            x_axis_type="datetime",
            title=f"{symbol}, {timeframe}, MACDH",
            plot_width=600,
            plot_height=150,
            tools=TOOLS,
            # sizing_mode="stretch_both",
            active_scroll="xwheel_zoom",
            active_drag="xpan",
            x_range=fig.x_range,
            sizing_mode="stretch_both",
            height_policy="max",
        )
        mfi_fig = figure(
            x_axis_type="datetime",
            title=f"{symbol}, {timeframe}, MFI14",
            plot_width=600,
            plot_height=150,
            tools=TOOLS,
            # sizing_mode="stretch_both",
            active_scroll="xwheel_zoom",
            active_drag="xpan",
            x_range=fig.x_range,
            sizing_mode="stretch_both",
            height_policy="max",
        )

        hist_line = macd_fig.line(
            "date",
            "MACDh_12_26_9",
            source=source,
            color="black",
            line_width=1.5,
            line_alpha=1.0,
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
        mfi_line = mfi_fig.line(
            "date",
            "MFI_14",
            source=source,
            color="green",
            line_alpha=1.0,
            name="mfi_line",
        )

        D1h_fig = figure(
            x_axis_type="datetime",
            title=f"{symbol}, {timeframe}, 1st MACDh derivative",
            plot_width=600,
            plot_height=150,
            tools=TOOLS,
            # sizing_mode="stretch_both",
            active_scroll="xwheel_zoom",
            active_drag="xpan",
            x_range=fig.x_range,
            sizing_mode="stretch_both",
            height_policy="max",
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
            tools=TOOLS,
            # sizing_mode="stretch_both",
            active_scroll="xwheel_zoom",
            active_drag="xpan",
            x_range=fig.x_range,
            sizing_mode="stretch_both",
            height_policy="max",
        )
        D2h_line = D2h_fig.line(
            "date",
            "D2h",
            source=source,
            color="blue",
            line_alpha=1.0,
            name="D2h_line",
        )

        hlc_source = ColumnDataSource(
            {"Index": self.df.index, "High": self.df.csup, "Low": self.df.cinf}
        )

        # ysize_source = ColumnDataSource(
        #     {"Index": self.ohlcv.index, "High": self.ohlcv.high, "Low": self.ohlcv.low}
        # )

        callback = lambda fig, source: (
            CustomJS(
                args={"y_range": fig.y_range, "source": source},
                code="""
            clearTimeout(window._autoscale_timeout);

            var Index = source.data.Index,
                Low = source.data.Low,
                High = source.data.High,
                start = cb_obj.start,
                end = cb_obj.end,
                min = Infinity,
                max = -Infinity;

            for (var i=0; i < Index.length; ++i) {
                if (start <= Index[i] && Index[i] <= end) {
                    max = Math.max(High[i], max);
                    min = Math.min(Low[i], min);
                }
            }
            var pad = (max - min) * .05;

            window._autoscale_timeout = setTimeout(function() {
                y_range.start = min - pad;
                y_range.end = max + pad;
            });
        """,
            )
        )

        # Finalise the figure
        fig.x_range.js_on_change("start", callback(fig, hlc_source))
        select.x_range.js_on_change("start", callback(select, hlc_source))
        figs = [fig, macd_fig, D1h_fig, D2h_fig, mfi_fig, select]
        dict_figs = {
            # ("csup", "cmed", "cinf", "close"): fig,
            ("MACD_12_26_9", "MACDh_12_26_9", "MACDs_12_26_9"): macd_fig,
            ("D1h",): D1h_fig,
            ("D2h",): D2h_fig,
            ("MFI_14",): mfi_fig,
        }

        # def set_figs_sources(dict_figs):
        #     for k, v in dict_figs.items():
        #         highs = self.df[list(v)].max().max()
        #         lows = highs = self.df[list(v)].min().min()
        #         fig_src = ColumnDataSource(
        #             {"Index": self.df.index, "High": self.df.csup, "Low": self.df.cinf}
        #         )

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
