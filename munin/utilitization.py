#!/usr/bin/env python
import sys
import os
lib = os.getenv("LITTLEFIELD_PATH")
if lib is not None:
    sys.path.append(lib)
from littlefield import Littlefield

def avg(data, size):
    return sum(data[((size*-1)-1):-1])/size

config = False
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True
if config:
    print("""graph_title Station Utilitization
graph_info Shows the utilitization of each station
graph_category littlefield
graph_vlabel Percent
""")

littlefield = Littlefield(os.getenv("LITTLEFIELD_USER"), os.getenv("LITTLEFIELD_PW"))
for station in range(1, 4):
    if config:
        print("station%s.label Station %s" % (station, station))
        print("station%s.warning 10:80" % station)
        print("station%s-3.label Station %s (3 day average)" % (station, station))
        print("station%s-3.warning 10:80" % station)
        print("station%s-10.label Station %s" % (station, station))
        print("station%s-10.warning 10:80" % station)
    else:
        util = littlefield.get_data("S%sUTIL" % station)['average']
        print("station%s.value %s" % (station, util[-1]*100))
        print("station%s-3.value %s" % (station, avg(util, 3)*100))
        print("station%s-10.value %s" % (station, avg(util, 10)*100))
