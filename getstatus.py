#!/usr/bin/env python
from littlefield import Littlefield
from configparser import ConfigParser

config = ConfigParser()
config.read(['littlefield.ini'])

littlefield = Littlefield(config['littlefield']['user'], config['littlefield']['password'])

status = littlefield.get_status()
for key, value in status.items():
    print("%s:\t%s" % (key, value))


def avg(data, size):
    return sum(util[((size*-1)-1):-1])/size

print("Station\t\t1 day avg\t3 day avg\t10 day avg")
for station in range(1, 4):
    machines = littlefield.get_station(station)['number of machines']
    util = littlefield.get_data("S%sUTIL" % (station))['average']
    print("Station %s:\t[ %.2f%% ]\t[ %.2f%% ]\t[ %.2f%% ] (%s machines)" %
          (station, (util[-1]*100), (avg(util, 3)*100), (avg(util, 10)*100), machines))
