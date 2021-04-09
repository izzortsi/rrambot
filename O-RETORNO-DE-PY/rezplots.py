from bokeh.io import output_file 
from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter
from bokeh.plotting import figure
from bokeh.layouts import gridplot

def simple_plot(df, name="filename.html"):
    
    output_file(f"${name}")

    labels = df.columns
    source = ColumnDataSource(df)

    TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset"

    ##
    # create a new plot and add a renderer
    fig = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, plot_height=1000, title="closes with indicators")
    for lab in labels:
        fig.line('date', lab, source=source)
    ##
    
    return fig

def ti_plot(df, name="filename.html"):
    
    output_file(f"${name}")

    labels = df.columns
    source = ColumnDataSource(df)

    TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"

    ##
    # create a new plot and add a renderer
    fig = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, plot_height=1000, title="closes with indicators")
    for lab in labels:
        fig.line('date', lab, source=source)
    ##
    fig.add_tools(HoverTool(
        tooltips=[
            ( 'time',   '@date{%m/%d %H:%M}'            ),
            ( 'close',  '$@{close}{%0.2f}' ), # use @{ } for field names with spaces
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
    
    return fig


def composite_plot(ohlcv, name="filename.html"):
    
    output_file(f"${name}")

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
    
    return p
