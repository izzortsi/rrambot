##
import pandas as pd
import pandas_ta as ta

# from binance.client import Client
# from binance.enums import *
# from grabber import *
##
from bokeh.io import output_file, show
from bokeh.models import *
from bokeh.plotting import figure
from bokeh.layouts import gridplot, column

##
from typing import Union, Callable

numeric = Union[int, float]


##
class Looker:
    def __init__(self, df, symbol, tframe, fromdate, todate):
        self.df = df
        self.symbol = symbol
        self.tframe = tframe
        self.fromdate = fromdate
        self.todate = todate

    def look(self, trades=None):

        source = ColumnDataSource(data=self.df)
        datasize = len(self.df)
        range_tool_a = datasize // 5
        range_tool_b = datasize // 3
        TOOLS = "crosshair, pan, wheel_zoom, box_zoom, reset, box_select, lasso_select"

        hover = HoverTool(
            tooltips=[
                ("time", "@date{%m/%d %H:%M}"),
                ("close", "$@{close}{%0.2f}"),  # use @{ } for field names with spaces
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

        subhover = HoverTool(
            tooltips=[
                ("time", "@date{%m/%d %H:%M}"),
                (
                    "histogram",
                    "@{histogram}{%0.2f}",
                ),  # use @{ } for field names with spaces
            ],
            formatters={
                "@date": "datetime",  # use 'datetime' formatter for '@date' field
                "@{histogram}": "printf",  # use 'printf' formatter for '@{adj close}' field
                # use default 'numeral' formatter for other fields
            },
            # display a tooltip whenever the cursor is vertically in line with a glyph
            mode="vline",
            line_policy="nearest",
            names=["histogram"],
        )

        cylims = (min(self.df.close), max(self.df.close))
        fig = figure(
            x_axis_type="datetime",
            title=f"{self.symbol}, {self.tframe}, from {self.fromdate} to {self.todate}",
            plot_width=950,
            plot_height=400,
            tools=[
                "crosshair",
                "pan",
                "box_zoom",
                "wheel_zoom",
                "save",
                "reset",
                hover,
            ],
            active_scroll="wheel_zoom",
            x_range=(
                self.df.close.index[range_tool_a],
                self.df.close.index[range_tool_b],
            ),
            y_range=cylims,
        )
        # hylims = (min(self.df.histogram[self.df.histogram.notna()])*0.95, (max(self.df.histogram[self.df.histogram.notna()])*1.05))

        subfig = figure(
            x_axis_type="datetime",
            title="MACD histogram",
            plot_width=950,
            plot_height=150,
            tools=[
                "crosshair",
                "pan",
                "box_zoom",
                "wheel_zoom",
                "save",
                "reset",
                subhover,
            ],
            active_scroll="wheel_zoom",
            x_range=fig.x_range,
        )

        cline = fig.line("date", "close", source=source, color="black", name="cprices")

        hist = subfig.line(
            "date", "histogram", source=source, color="red", name="histogram"
        )

        hist_zero = Span(
            location=0,
            dimension="width",
            line_color="green",
            line_dash="dashed",
            line_width=3,
        )
        subfig.add_layout(hist_zero)
        # csline = fig.line('date', 'csup', source= source, color='green', line_alpha=0.8, line_dash = "dashed", name='cs')
        # cmline = fig.line('date', 'cmed', source= source, color='blue', line_alpha=0.8, line_dash = "dashed", name='cm')
        # ciline = fig.line('date', 'cinf', source= source, color='red', line_alpha=0.8, line_dash = "dashed", name='ci')

        select = figure(
            title="Drag the middle and edges of the selection box to change the range above",
            plot_height=100,
            plot_width=950,  # y_range=fig.y_range,
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

        if trades != None:
            for i, trade in enumerate(trades[:-1]):
                entry_date = trade[0]
                entry_float = entry_date.timestamp() * 1000
                entry_price = self.df.loc[self.df.index == entry_date]["close"].values[
                    0
                ]

                exit_date = trade[1]
                exit_float = exit_date.timestamp() * 1000
                exit_price = self.df.loc[self.df.index == exit_date]["close"].values[0]

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
                profit = ((exit_price - entry_price) / entry_price) * 100
                citation = Label(
                    x=(entry_float + exit_float) / 2,
                    y=(entry_price + exit_price) / 2,
                    text=f"T{i+1}: {profit:.3f}%",
                    render_mode="canvas",
                    border_line_color="black",
                    border_line_alpha=0.0,
                    background_fill_color="white",
                    background_fill_alpha=0.0,
                    text_font_size="8px",
                )
                fig.add_layout(citation)

        p = column(fig, subfig, select)
        # show(p)
        return p


##
# looker = Looker(df)

##
# p = looker.look()

##
# show(p)
##

##
