#!/usr/bin/env python
from littlefield import Littlefield
from configparser import ConfigParser
import notify

config = ConfigParser()
config.read(['littlefield.ini'])

littlefield = Littlefield(config['littlefield']['user'], config['littlefield']['password'])

for i in range(1, 4):
    station = littlefield.get_station(i)
    utilitization = littlefield.get_data("S%sUTIL" % i)['average'][-1]
    if utilitization > float(config['littlefield']['util_high']):
        machines = station['number of machines'] + 1
        notify.send("Station %s has a utilitization of %s. Increasing machines from %s to %s" %
                    (i, utilitization, station['number of machines'], machines))
        littlefield.update_machine_count(station, machines)
    elif utilitization < float(config['littlefield']['util_low']) and station['number of machines'] > 1:
        machines = station['number of machines'] - 1
        notify.send("Station %s has a utilitization of %s. Decreasing machines from %s to %s" %
                    (i, utilitization, station['number of machines'], machines))
        littlefield.update_machine_count(station, machines)
