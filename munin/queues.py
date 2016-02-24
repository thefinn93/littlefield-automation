#!/usr/bin/env python
import sys
import os
lib = os.getenv("LITTLEFIELD_PATH")
if lib is not None:
    sys.path.append(lib)
from littlefield import Littlefield

def avg(data, size):
    return sum(util[((size*-1)-1):-1])/size

config = False
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True
if config:
    print("""graph_title Queue Size
graph_info Shows the queue size
graph_category littlefield
graph_vlabel Kits
""")

littlefield = Littlefield(os.getenv("LITTLEFIELD_USER"), os.getenv("LITTLEFIELD_PW"))
for station in range(1, 4):
    if config:
        print("station%s.label Station %s" % (station, station))
        print("station%s-3.label Station %s (3 day average)" % (station, station))
        print("station%s-10.label Station %s (10 day average)" % (station, station))
    else:
        size = littlefield.get_data("S%sQ" % station)['average']
        print("station%s.value %s" % (station, size[-1]))
        print("station%s-3.value %s" % (station, avg(size, 3)))
        print("station%s-10.value %s" % (station, avg(size, 10)))
