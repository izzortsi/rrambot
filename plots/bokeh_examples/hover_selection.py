from bokeh.models.tools import HoverTool

from bokeh.sampledata.glucose import data

subset = data.loc["2010-10-06"]

x, y = subset.index.to_series(), subset["glucose"]

# Basic plot setup
p = figure(width=600, height=300, x_axis_type="datetime", title="Hover over points")

p.line(x, y, line_dash="4 4", line_width=1, color="gray")

cr = p.circle(
    x,
    y,
    size=20,
    fill_color="grey",
    hover_fill_color="firebrick",
    fill_alpha=0.05,
    hover_alpha=0.3,
    line_color=None,
    hover_line_color="white",
)

p.add_tools(HoverTool(tooltips=None, renderers=[cr], mode="hline"))

show(p)
