##
import pandas as pd
import pandas_ta as ta

# from binance.client import Client
# from binance.enums import *
# from grabber import *
##
from bokeh.io import output_file, show, save
from bokeh.models import *
from bokeh.plotting import figure
from bokeh.layouts import gridplot, column

##
from typing import Union, Callable

numeric = Union[int, float]


# %%


df_trades = pd.read_csv(
    f"{pwd()}/logs/208-21_17-52-33/macd_bnbusdt_1m-17-52-36.csv",
    parse_dates=["entry_time", "exit_time"],
)
df = pd.read_csv(
    f"{pwd()}/logs/208-21_17-52-33/macd_bnbusdt_1m-17-52-36_candles.csv",
    parse_dates=["date"],
)

# %%


class FTestLooker:
    def __init__(self, df, trades, symbol, leverage):
        self.df = df
        self.trades = trades
        self.symbol = symbol
        self.tframe = "<1m"
        self.fromdate = df.date.iloc[0]
        self.todate = df.date.iloc[-1]
        self.leverage = leverage

    def look(self):

        source = ColumnDataSource(data=self.df)
        datasize = len(self.df)
        TOOLS = "crosshair, pan, wheel_zoom, box_zoom, reset, box_select, lasso_select"
        a = datasize // 5
        b = datasize // 3
        range_tool_a = self.df.date.iloc[a]
        range_tool_b = self.df.date.iloc[b]
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
            ],
            active_scroll="wheel_zoom",
            x_range=(
                range_tool_a,
                range_tool_b,
            ),
            y_range=cylims,
        )

        cline = fig.line("date", "close", source=source, color="black")

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

        # select.line('date', 'csup', source=source)
        # select.line('date', 'cmed', source=source)
        # select.line('date', 'cinf', source=source)
        select.ygrid.grid_line_color = None
        select.add_tools(range_tool)
        select.toolbar.active_multi = range_tool
        cprofylims = (
            min(self.trades.cumulative_profit),
            max(self.trades.cumulative_profit),
        )
        cumprof = figure(
            x_axis_type="datetime",
            title="cumulative profit (%)",
            plot_width=1200,
            plot_height=150,
            tools=[
                "crosshair",
                "reset",
            ],
            x_range=fig.x_range,
            y_range=cprofylims,
        )

        prof_line = cumprof.line(
            self.trades.exit_time, self.trades.cumulative_profit, color="black"
        )

        diffylims = (
            min(self.trades.percentual_difference),
            max(self.trades.percentual_difference),
        )
        diffs = figure(
            x_axis_type="datetime",
            title="percentual differences",
            plot_width=1200,
            plot_height=150,
            tools=[
                "crosshair",
                "reset",
            ],
            x_range=fig.x_range,
            y_range=diffylims,
        )

        diffs_line = diffs.line(
            self.trades.exit_time, self.trades.percentual_difference, color="black"
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
                text=f"{self.trades.percentual_difference.iloc[i]:.3f}%",
                render_mode="canvas",
                border_line_color="black",
                border_line_alpha=0.0,
                background_fill_color="white",
                background_fill_alpha=0.0,
                text_font_size="7px",
            )
            fig.add_layout(citation)

        p = column(fig, cumprof, diffs, select)
        return p


# %%


##
looker = FTestLooker(df, df_trades, "bnbusdt", 100)
output_file(
    f"{looker.symbol}_1s_from={looker.fromdate}_to={looker.todate}.html".replace(
        " ", "_"
    )
)

# %%

p = looker.look()

# %%

show(p)
save(p)
