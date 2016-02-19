#!/usr/bin/env python
from littlefield import Littlefield
from configparser import ConfigParser

config = ConfigParser()
config.read(['littlefield.ini'])

littlefield = Littlefield(config['littlefield']['user'], config['littlefield']['password'])

print(littlefield.get_status())

for station in range(1, 4):
    print("Station %s" % station)
    print(littlefield.get_station(station))
    print(littlefield.get_data("S%sUTIL" % (station))['average'][-1])
