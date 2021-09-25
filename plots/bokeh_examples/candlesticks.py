from math import pi
from bokeh.plotting import figure
from bokeh.io import output_notebook,show
from bokeh.resources import INLINE

output_notebook(resources=INLINE)

inc = apple_df.Close > apple_df.Open
dec = apple_df.Open > apple_df.Close

w = 12*60*60*1000

p = figure(x_axis_type="datetime", plot_width=800, plot_height=500, title = "Apple, March - 2020")

p.segment(apple_df.index, apple_df.High, apple_df.index, apple_df.Low, color="black")

p.vbar(apple_df.index[inc], w, apple_df.Open[inc], apple_df.Close[inc], fill_color="lawngreen", line_color="red")

p.vbar(apple_df.index[dec], w, apple_df.Open[dec], apple_df.Close[dec], fill_color="tomato", line_color="lime")

show(p)