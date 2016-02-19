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
    print(littlefield.get_station(station))
    util = littlefield.get_data("S%sUTIL" % (station))['average']
    print("Utilitization: %s %s %s" % (util[-1], avg(util, 3), avg(util, 10)))
