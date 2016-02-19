#!/usr/bin/env python
from littlefield import Littlefield
from configparser import ConfigParser

config = ConfigParser()
config.read(['littlefield.ini'])

littlefield = Littlefield(config['littlefield']['user'], config['littlefield']['password'])

print(littlefield.get_status())


def avg(data, size):
    return sum(util[((size*-1)-1):-1])/size

for station in range(1, 4):
    print("Station %s" % station)
    machines = littlefield.get_station(station)['number of machines']
    util = littlefield.get_data("S%sUTIL" % (station))['average']
    print("Utilitization: [ %.2f%% ]\t[ %.2f%% ]\t[ %.2f%% ] (%s machines)" %
          ((util[-1]*100), (avg(util, 3)*100), (avg(util, 10)*100), machines))
