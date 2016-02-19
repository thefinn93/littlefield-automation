#!/usr/bin/env python
from littlefield import Littlefield
from configparser import ConfigParser
from bokeh.plotting import figure, output_server, show, gridplot

config = ConfigParser()
config.read(['littlefield.ini'])

littlefield = Littlefield(config['littlefield']['user'], config['littlefield']['password'])
output_server("littlefield")

datatypes = [
    "JOBIN",    # Number of jobs accepted per day
    "JOBQ",     # Number of jobs waiting
    "INV",      # Inventory levels
    "JOBOUT",   # Number of completed jobs
    "JOBT",     # Lead times
    "JOBREV",   # Revenue
    "S1Q",      # Number of kits queued for station 1
    "S1UTIL",   # Station 1 utilitization by day
    "S2Q",      # number of kits queued for station 2
    "S2UTIL",   # Station 2 utilitization by day
    "S3Q",      # number of kits queued for station 3
    "S3UTIL"    # Station 3 utilitization by day
]

plots = []
for datatype in datatypes:
    print(datatype)
    data = littlefield.get_data(datatype)
    keys = list(data.keys())
    p = figure(
        tools="pan,box_zoom,reset,save", title=datatype, x_axis_label=keys[1], y_axis_label=keys[0]
    )
    p.line(data[keys[1]], data[keys[0]], legend=datatype)
    plots.append(p)

show(gridplot([plots], toolbar_location=None))
