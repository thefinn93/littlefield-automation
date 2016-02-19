#!/usr/bin/env python
from littlefield import Littlefield
from configparser import ConfigParser
import notify

config = ConfigParser()
config.read(['littlefield.ini'])

THRESHOLD_HIGH = 0.7
THRESHOLD_LOW = 0.2

littlefield = Littlefield(config['littlefield']['user'], config['littlefield']['password'])

print(littlefield.get_status())

for i in range(1, 4):
    station = littlefield.get_station(i)
    utilitization = littlefield.get_data("S%sUTIL" % i)['average'][-1]
    if utilitization > THRESHOLD_HIGH:
        machines = station['number of machines'] + 1
        notify.send("Station %s has a utilitization of %s. Increasing machines from %s to %s" %
                    (i, utilitization, station['number of machines'], machines))
        littlefield.update_machine_count(station, machines)
    elif utilitization < THRESHOLD_LOW and station['number of machines'] > 1:
        notify.send("Station %s has a utilitization of %s. Maybe we should sell a machine" %
                    (i, utilitization))
