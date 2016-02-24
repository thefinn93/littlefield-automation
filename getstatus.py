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

print("Station\t\t1 day avg\t\t3 day avg\t\t10 day avg")
for station in range(1, 4):
    machines = littlefield.get_station(station)['number of machines']
    util = littlefield.get_data("S%sUTIL" % station)['average']
    queue = littlefield.get_data("S%sQ" % station)['average']
    print("Station %s:\t[ %.2f%% | %.2f ]\t[ %.2f%% | %.2f ]\t[ %.2f%% | %.2f ] (%s machines)" %
          (station, (util[-1]*100), queue[-1], (avg(util, 3)*100), avg(queue, 3), (avg(util, 10)*100), avg(queue, 10), machines))

jobt = littlefield.get_data("JOBT")['average']
print("Job Times:\t[ %.2f ]\t\t[ %.2f ]\t\t[ %.2f ]" % (jobt[-1], avg(jobt, 3), avg(jobt, 10)))

jobq = littlefield.get_data("JOBQ")['average']
print("Queue Size:\t[ %.2f ]\t\t[ %.2f ]\t\t[ %.2f ]" % (jobq[-1], avg(jobq, 3), avg(jobq, 10)))
