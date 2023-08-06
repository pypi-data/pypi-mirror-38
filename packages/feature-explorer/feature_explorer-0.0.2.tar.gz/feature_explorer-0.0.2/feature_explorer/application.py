from flask import Flask, render_template, request
from threading import Thread
import pickle
from bokeh.embed import server_document
from bokeh.layouts import widgetbox, layout
from bokeh.models import ColumnDataSource, Slider, Range1d, LinearAxis
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.models.widgets import (
    Select, Div, CheckboxButtonGroup, TextInput
)
from tornado.ioloop import IOLoop
from bokeh.palettes import Category20

import numpy as np
import pandas as pd
from scipy import stats

app = Flask(__name__)

def read_pickle(filename):
    with open(filename, 'rb') as handle:
        return(pickle.load(handle))

@app.route('/', methods=['GET'])
def index():
    return render_template("pages/index.html", file_uploaded=False)

@app.route('/data_upload', methods=['POST'])
def data_upload():
    if request.method == 'POST':
        global df
        f = request.files['file']
        df = pd.read_csv(f)
        return render_template("pages/index.html", file_uploaded=True)

@app.route('/scatter', methods=['GET'])
def scatter():
    plot = server_document('http://localhost:5006/scatter')
    return render_template("pages/scatter.html", plot=plot)

@app.route('/dependence', methods=['GET'])
def dependence():
    plot = server_document('http://localhost:5006/dependence')
    return render_template("pages/dependence.html", plot=plot)

def scatter_bk(doc):

    def make_plot(
            df=df,
            x=df.columns[0],
            y=df.columns[1],
            x_transform='raw',
            y_transform='raw',
            plot_height=500,
            plot_width=500
    ):
        df_to_plot = df.copy()
        x_label = ''
        y_label = ''

        # error messages
        x_is_categorical = not np.issubdtype(df_to_plot[x].dtype, np.number)
        y_is_categorical = not np.issubdtype(df_to_plot[y].dtype, np.number)
        if x_is_categorical:
            return(Div(text='<font color="red"><br><b>X should be numeric'))
        if y_is_categorical:
            return(Div(text='<font color="red"><br><b>Y should be numeric'))

        # apply selected transformations
        if x_transform == 'sqrt':
            df_to_plot[x] = np.sqrt(df_to_plot[x])
            x_label = ' (sqrt) '
        if x_transform == 'square (^2)':
            df_to_plot[x] = df_to_plot[x]**2
            x_label = ' (^2) '
        if x_transform == 'cube (^3)':
            df_to_plot[x] = df_to_plot[x]**3
            x_label = ' (^3) '
        if x_transform == 'log':
            df_to_plot[x] = np.log(df_to_plot[x])
            x_label = ' (log) '
        if x_transform == 'standardize (z-score)':
            df_to_plot[x] = stats.zscore(df_to_plot[x])
            x_label = ' (standardized) '

        if y_transform == 'sqrt':
            df_to_plot[y] = np.sqrt(df_to_plot[y])
            y_label = ' (sqrt) '
        if y_transform == 'square (^2)':
            df_to_plot[y] = df_to_plot[y]**2
            y_label = ' (^2) '
        if x_transform == 'cube (^3)':
            df_to_plot[y] = df_to_plot[y]**3
            y_label = ' (^3) '
        if y_transform == 'log':
            df_to_plot[y] = np.log(df_to_plot[y])
            y_label = ' (log) '
        if y_transform == 'standardize (z-score)':
            df_to_plot[y] = stats.zscore(df_to_plot[y])
            y_label = ' (standardized) '


        # make figure
        source = ColumnDataSource(data=df_to_plot)
        plot = figure(
            title=x + x_label + ' vs ' + y + y_label,
            plot_height=plot_height,
            plot_width=plot_width,
            tools="pan, wheel_zoom, box_zoom, reset, previewsave",
        )

        plot.circle(
            x=x,
            y=y,
            source=source
        )

        plot.xaxis.axis_label = str(x) + x_label
        plot.yaxis.axis_label = str(y) + y_label

        return plot

    plot = make_plot()

    def callback(attr, old, new):
        plot = make_plot(
            x=select_x.value,
            y=select_y.value,
            plot_height=int(plot_height.value),
            plot_width=int(plot_width.value),
            x_transform=transform_x.value,
            y_transform=transform_y.value,
        )
        page_layout.children[0].children[1] = plot

    # select widget
    select_div = Div(text='<b>Select Fields</b>')
    select_options = list(df.columns)
    select_x = Select(title="X-axis", options=select_options , value=df.columns[0])
    select_y = Select(title="Y-Axis", options=select_options , value=df.columns[1])
    select_x.on_change('value', callback)
    select_y.on_change('value', callback)

    # transformation widgets
    transform_div = Div(text='<br><br><b>Data Transformations</b>')
    transform_options = ['raw', 'log', 'sqrt', 'square (^2)', 'cube (^3)', 'standardize (z-score)']
    transform_x = Select(title="X:", options=transform_options, value='raw')
    transform_y = Select(title="Y:", options=transform_options, value='raw')
    transform_x.on_change('value', callback)
    transform_y.on_change('value', callback)

    # plot output options
    plot_options_div = Div(text='<br><br><b>Plot Options:</b>')
    plot_height = TextInput(value='500', title='Plot Height')
    plot_height.on_change('value', callback)
    plot_width = TextInput(value='500', title='Plot Width')
    plot_width.on_change('value', callback)

    # widgets all grouped together
    widgets = widgetbox(
        select_div, select_x, select_y,
        transform_div, transform_x, transform_y,
        plot_options_div, plot_height, plot_width
    )

    # make page layout
    page_layout = layout(
        [[widgets, plot]]
    )
    doc.add_root(page_layout)

def dependence_bk(doc):

    def make_plot(
            df=df,
            x=df.columns[0],
            y=df.columns[1],
            x_transform='raw',
            y_transform='raw',
            x_bins=5,
            show_bins=True,
            plot_width=500,
            plot_height=500,
            legend_location=None,
    ):
        df_to_plot = df.copy()
        x_label = ''
        y_label = ''

        # remove any observations with nulls
        df_to_plot = (
            df_to_plot[(~pd.isnull(df_to_plot[x])) & (~pd.isnull(df_to_plot[y]))]
        )

        x_is_categorical = not np.issubdtype(df_to_plot[x].dtype, np.number)
        y_is_categorical = not np.issubdtype(df_to_plot[y].dtype, np.number)

        # error messages
        if x == y:
            return (Div(text='<font color="red"><br><b>X and Y variables must be different'))

        if x_is_categorical:
            return (Div(text='<font color="red"><br><b>X variable must be numeric'))

        if y_is_categorical:
            unique_values_y = list(np.unique(df_to_plot[y]))
            y_colors = Category20[max(3, len(unique_values_y))]
            if len(unique_values_y) < 2:
                return(Div(text='<font color="red"><br><b>Y has only one category'))

            for category in unique_values_y:
                df_to_plot[category] = (df_to_plot[y] == category)*1

        # apply selected transformations if fields are numeric
        if not x_is_categorical:
            if x_transform == 'sqrt':
                df_to_plot[x] = np.sqrt(df_to_plot[x])
                x_label = ' (sqrt) '
            if x_transform == 'square (^2)':
                df_to_plot[x] = df_to_plot[x]**2
                x_label = ' (^2) '
            if x_transform == 'cube (^3)':
                df_to_plot[x] = df_to_plot[x]**3
                x_label = ' (^3) '
            if x_transform == 'log':
                df_to_plot[x] = np.log(df_to_plot[x])
                x_label = ' (log) '
            if x_transform == 'standardize (z-score)':
                df_to_plot[x] = stats.zscore(df_to_plot[x])
                x_label = ' (standardized) '

        if not y_is_categorical:
            if y_transform == 'sqrt':
                df_to_plot[y] = np.sqrt(df_to_plot[y])
                y_label = ' (sqrt) '
            if y_transform == 'square (^2)':
                df_to_plot[y] = df_to_plot[y]**2
                y_label = ' (^2) '
            if x_transform == 'cube (^3)':
                df_to_plot[y] = df_to_plot[y]**3
                y_label = ' (^3) '
            if y_transform == 'log':
                df_to_plot[y] = np.log(df_to_plot[y])
                y_label = ' (log) '
            if y_transform == 'standardize (z-score)':
                df_to_plot[y] = stats.zscore(df_to_plot[y])
                y_label = ' (standardized) '

        # slice into bins
        bin_interval = (np.max(df_to_plot[x]) - np.min(df_to_plot[x]))/x_bins
        bins_x = np.arange(np.min(df_to_plot[x])-.01, np.max(df_to_plot[x]), bin_interval)
        df_to_plot[x] = pd.cut(df_to_plot[x], bins_x)

        # aggregate df
        if y_is_categorical:
            df_to_plot = (
                df_to_plot[[x] + unique_values_y]
                    .groupby([x], as_index=False)
                    .agg(
                    [np.mean, np.size]
                )
            ).reset_index()
        else:
            df_to_plot = (
                df_to_plot[[x, y]]
                    .groupby([x], as_index=False)
                    .agg({
                    y: [np.mean, np.size]
                })
            )

        df_to_plot[x] = df_to_plot[x].astype('str')

        # make figure
        source = ColumnDataSource(data=df_to_plot)
        plot = figure(
            title=x + x_label + ' vs ' + y + y_label,
            x_range=list(df_to_plot[x]),
            plot_height=plot_height,
            plot_width=plot_width
        )

        # add two ranges
        if y_is_categorical:
            plot.y_range = Range1d(start=0, end=1)
        else:
            plot.y_range = Range1d(start=0, end=np.max(df_to_plot[y]['mean']) + np.max(df_to_plot[y]['mean'])*.1)

        # plot data points
        if y_is_categorical:
            for idx, category in enumerate(unique_values_y):
                plot.line(
                    x=x + '_',
                    y=category + '_mean',
                    source=source,
                    legend=category,
                    color=y_colors[idx]
                )

                if legend_location is not None:
                    plot.legend.location = legend_location

                plot.circle(
                    x=x + '_',
                    y=category + '_mean',
                    source=source,
                    color=y_colors[idx]
                )
        else:
            plot.line(
                x=x + '_',
                y=y + '_mean',
                source=source
            )

            plot.circle(
                x=x + '_',
                y=y + '_mean',
                source=source
            )

        if show_bins:
            if y_is_categorical:
                y = unique_values_y[0]

            plot.vbar(
                x=x + '_',
                top=y + '_size',
                width=.5,
                alpha=.15,
                y_range_name='bin_size',
                source=source
            )

            plot.extra_y_ranges = {
                'bin_size': Range1d(
                    start=0,
                    end=np.max(df_to_plot[y]['size']) + np.max(df_to_plot[y]['size'])*.1
                )
            }
            plot.add_layout(
                LinearAxis(y_range_name='bin_size'), 'right',
            )

        plot.xaxis.axis_label = str(x) + x_label
        plot.xaxis.major_label_orientation = 3.14159 / 4
        if y_is_categorical:
            plot.yaxis[0].axis_label = 'percentage in class'
            plot.yaxis[1].axis_label = 'bin size'
        else:
            plot.yaxis.axis_label = str(y) + y_label

        return plot

    plot = make_plot()

    def callback(attr, old, new):
        plot = make_plot(
            x=select_x.value,
            y=select_y.value,
            x_transform=transform_x.value,
            y_transform=transform_y.value,
            x_bins=bins_slider.value,
            show_bins=plot_options.active[0],
            plot_height=int(plot_height.value),
            plot_width=int(plot_width.value),
            legend_location=legend_select.value
        )
        page_layout.children[0].children[1] = plot

    # select widget
    select_div = Div(text='<b>Select Fields</b>')
    select_options = list(df.columns)
    select_x = Select(title="X-axis", options=select_options , value=df.columns[0])
    select_y = Select(title="Y-Axis", options=select_options , value=df.columns[1])
    select_x.on_change('value', callback)
    select_y.on_change('value', callback)

    # transformation widgets
    transform_div = Div(text='<br><br><b>Data Transformations</b>')
    transform_options = ['raw', 'log', 'sqrt', 'square (^2)', 'cube (^3)', 'standardize (z-score)']
    transform_x = Select(title="X:", options=transform_options, value='raw')
    transform_y = Select(title="Y:", options=transform_options, value='raw')
    transform_x.on_change('value', callback)
    transform_y.on_change('value', callback)

    # bins widgets
    bins_div = Div(text='<br><br><b>Select Number of Bins:</b>')
    bins_slider = Slider(value=5, start=2, end=20, step=1)
    bins_slider.on_change('value', callback)

    # plot output options
    plot_options_div = Div(text='<br><br><b>Plot Options:</b>')
    plot_options = CheckboxButtonGroup(
        labels=['Hide Bins'], active=[1]
    )
    plot_options.on_change('active', callback)
    plot_height = TextInput(value='500', title='Plot Height')
    plot_height.on_change('value', callback)
    plot_width = TextInput(value='500', title='Plot Width')
    plot_width.on_change('value', callback)

    legend_options = ["top_left", "top_center", "top_right", "center_right",
                      "bottom_right", "bottom_center", "bottom_left", "center_left",
                      "center"]
    legend_select = Select(title="Legend Location", options=legend_options, value=legend_options[2])
    legend_select.on_change('value', callback)

    # widgets all grouped together
    widgets = widgetbox(
        select_div, select_x, select_y,
        transform_div, transform_x, transform_y,
        bins_div, bins_slider,
        plot_options_div, plot_options, legend_select, plot_height, plot_width
    )

    # make page layout
    page_layout = layout(
        [[widgets, plot]]
    )
    doc.add_root(page_layout)

def bk_worker():
    server = Server(
        {
            '/scatter': scatter_bk,
            '/dependence': dependence_bk,
        },
        io_loop=IOLoop(),
        allow_websocket_origin=["localhost:5000", "127.0.0.1:5000"]
    )
    server.start()
    server.io_loop.start()

@app.before_first_request
def start_bokeh_server():
    Thread(target=bk_worker).start()
    print('bokeh server started')

if __name__ == '__main__':
    app.run()
