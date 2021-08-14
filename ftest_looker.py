##
import pandas as pd
import pandas_ta as ta
import os
import argparse

from bokeh.io import output_file, show, save
from bokeh.models import *
from bokeh.plotting import figure
from bokeh.layouts import gridplot, column
from typing import Union, Callable

numeric = Union[int, float]


class FTestLooker:
    def __init__(self, df, trades, symbol, leverage=100):
        self.df = df
        self.trades = trades
        self.symbol = symbol
        self.tframe = "1s"
        self.fromdate = df.date.iloc[0]
        self.todate = df.date.iloc[-1]
        self.leverage = leverage
        self.trades["unleveraged_percentual_difference"] = (
            (self.trades.exit_price - self.trades.entry_price)
            / self.trades.entry_price
            * 100
        )

    def look(self):

        source = ColumnDataSource(data=self.df)
        datasize = len(self.df)
        TOOLS = "crosshair, pan, wheel_zoom, box_zoom, reset, box_select, lasso_select"
        a = datasize // 5
        b = datasize // 3
        range_tool_a = self.df.date.iloc[a]
        range_tool_b = self.df.date.iloc[b]

        close_hover = HoverTool(
            tooltips=[
                # ("index", "$index"),
                ("time", "@date{%m/%d %H:%M:%S}"),
                ("close", "$@close{%0.4f}"),  # use @{ } for field names with spaces
            ],
            formatters={
                "@date": "datetime",  # use 'datetime' formatter for '@date' field
                "@close": "printf",  # use 'printf' formatter for '@{adj close}' field
                # use default 'numeral' formatter for other fields
            },
            # display a tooltip whenever the cursor is vertically in line with a glyph
            mode="vline",
            line_policy="nearest",
            names=["close"],
        )

        cylims = (min(self.df.close), max(self.df.close))

        fig = figure(
            x_axis_type="datetime",
            title=f"{self.symbol}",
            plot_width=1200,
            plot_height=400,
            tools=[
                "crosshair",
                "pan",
                "box_zoom",
                "wheel_zoom",
                "save",
                "reset",
                close_hover,
            ],
            active_scroll="wheel_zoom",
            x_range=(
                range_tool_a,
                range_tool_b,
            ),
            y_range=cylims,
        )

        cline = fig.line("date", "close", source=source, color="black", name="close")

        #######

        select = figure(
            title="Drag the middle and edges of the selection box to change the range above",
            plot_height=100,
            plot_width=1200,  # y_range=fig.y_range,
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

        select.ygrid.grid_line_color = None
        select.add_tools(range_tool)
        select.toolbar.active_multi = range_tool

        #######
        source2 = ColumnDataSource(data=self.trades)

        #######

        cprof_hover = HoverTool(
            tooltips=[
                # ("index", "$index"),
                ("exit time", "@exit_time{%m/%d %H:%M:%S}"),
                (
                    "cumulative profit (computed against x100 leveraging)",
                    "@cumulative_profit%",
                ),  # use @{ } for field names with spaces
            ],
            formatters={
                "@exit_time": "datetime",  # use 'datetime' formatter for '@date' field
                "@cumulative_profit": "numeral",  # use 'printf' formatter for '@{adj close}' field
                # use default 'numeral' formatter for other fields
            },
            # display a tooltip whenever the cursor is vertically in line with a glyph
            mode="vline",
            line_policy="nearest",
            names=["cprof"],
        )
        cprof_range = max(self.trades.cumulative_profit) - min(
            self.trades.cumulative_profit
        )
        cprofylims = (
            min(self.trades.cumulative_profit) - 0.1 * cprof_range,
            max(self.trades.cumulative_profit) + 0.1 * cprof_range,
        )

        cumprof = figure(
            x_axis_type="datetime",
            title="cumulative profit (%)",
            plot_width=1200,
            plot_height=250,
            tools=[
                "crosshair",
                "reset",
                cprof_hover,
            ],
            x_range=fig.x_range,
            y_range=cprofylims,
        )

        prof_line = cumprof.line(
            # self.trades.exit_time,
            # self.trades.cumulative_profit,
            "exit_time",
            "cumulative_profit",
            source=source2,
            color="black",
            name="cprof",
        )
        #######

        pdiff_hover = HoverTool(
            tooltips=[
                # ("index", "$index"),
                ("exit time", "@exit_time{%m/%d %H:%M:%S}"),
                (
                    "entry price",
                    "$@entry_price{0.0[0000]}",
                ),
                (
                    "exit price",
                    "$@exit_price{0.0[0000]}",
                ),
                (
                    "unleveraged percentual difference",
                    "@unleveraged_percentual_difference{0.0[0000]}%",
                ),
                (
                    f"percentual difference (leveraged by {self.leverage})",
                    "@percentual_difference{0.0[0000]}%",
                ),  # use @{ } for field names with spaces
            ],
            formatters={
                "@exit_time": "datetime",  # use 'datetime' formatter for '@date' field
                "@entry_price": "numeral",
                "@exit_price": "numeral",
                "@unleveraged_percentual_difference": "numeral",
                "@percentual_difference": "numeral",  # use 'printf' formatter for '@{adj close}' field
                # use default 'numeral' formatter for other fields
            },
            # display a tooltip whenever the cursor is vertically in line with a glyph
            mode="vline",
            line_policy="nearest",
            names=["pdiff"],
        )
        pdiff_range = max(self.trades.percentual_difference) - min(
            self.trades.percentual_difference
        )
        pdiffylims = (
            min(self.trades.percentual_difference) - 0.1 * pdiff_range,
            max(self.trades.percentual_difference) + 0.1 * pdiff_range,
        )

        pdiffs = figure(
            x_axis_type="datetime",
            title="percentual differences",
            plot_width=1200,
            plot_height=250,
            tools=[
                "crosshair",
                "reset",
                pdiff_hover,
            ],
            x_range=fig.x_range,
            y_range=pdiffylims,
        )

        pdiffs_line = pdiffs.line(
            # self.trades.exit_time,
            # self.trades.percentual_difference,
            "exit_time",
            "percentual_difference",
            source=source2,
            color="black",
            name="pdiff",
        )

        for i, trade in self.trades.iterrows():
            entry_float = pd.to_datetime(trade.entry_time).timestamp() * 1000
            entry_price = trade.entry_price

            exit_float = pd.to_datetime(trade.exit_time).timestamp() * 1000
            exit_price = trade.exit_price

            if exit_price > entry_price:
                poly = PolyAnnotation(
                    fill_color="green",
                    fill_alpha=0.3,
                    xs=[entry_float, entry_float, exit_float, exit_float],
                    ys=[
                        entry_price - abs(exit_price - entry_price) * 0.1,
                        entry_price + abs(exit_price - entry_price) * 0.1,
                        exit_price + abs(exit_price - entry_price) * 0.1,
                        exit_price - abs(exit_price - entry_price) * 0.1,
                    ],
                )
                fig.add_layout(poly)
            else:
                poly = PolyAnnotation(
                    fill_color="red",
                    fill_alpha=0.3,
                    xs=[entry_float, entry_float, exit_float, exit_float],
                    ys=[
                        entry_price - abs(exit_price - entry_price) * 0.1,
                        entry_price + abs(exit_price - entry_price) * 0.1,
                        exit_price + abs(exit_price - entry_price) * 0.1,
                        exit_price - abs(exit_price - entry_price) * 0.1,
                    ],
                )
                fig.add_layout(poly)

            profit = ((exit_price - entry_price) / entry_price) * 100 * self.leverage
            citation = Label(
                x=(entry_float + exit_float) / 2,
                y=(entry_price + exit_price) / 2,
                text=f"{self.trades.percentual_difference.iloc[i]:.2f}%",
                render_mode="canvas",
                border_line_color="black",
                border_line_alpha=0.0,
                background_fill_color="white",
                background_fill_alpha=0.0,
                text_font_size="7px",
            )
            fig.add_layout(citation)

        p = column(fig, cumprof, pdiffs, select)
        return p


# %%

# logdate = (
#     "208-21_17-52-33"  # formato: "%j-%y_%H-%M-%S"; ver src.utils.strf_epoch(epochtime)
# )
# log_filename_prefix = "macd_bnbusdt_1m-17-52-36"
# symbol = "bnbusdt"


def main():

    read_from = os.path.join(os.getcwd(), "logs", logdate)

    trades_data_path = os.path.join(read_from, f"{log_filename_prefix}.csv")

    df_trades = pd.read_csv(
        trades_data_path,
        parse_dates=["entry_time", "exit_time"],
    )

    candles_data_path = os.path.join(read_from, f"{log_filename_prefix}_candles.csv")

    df = pd.read_csv(
        candles_data_path,
        parse_dates=["date"],
    )

    looker = FTestLooker(df, df_trades, symbol)

    output_filename = f"{log_filename_prefix}_profitcheck.html"

    output_file(os.path.join(read_from, output_filename))

    p = looker.look()

    show(p)
    save(p)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--logdate", type=str)
    parser.add_argument("-p", "--filename_prefix", type=str)
    parser.add_argument("-s", "--symbol", type=str)
    # parser.add_argument("-L", "--leverage", default=100, type=int)
    args = parser.parse_args()

    logdate = args.logdate
    log_filename_prefix = args.filename_prefix
    symbol = args.symbol

    main()

