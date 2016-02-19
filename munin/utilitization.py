#!/usr/bin/env python
import sys
import os
lib = os.getenv("LITTLEFIELD_PATH")
if lib is not None:
    sys.path.append(lib)
from littlefield import Littlefield

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
    else:
        util = littlefield.get_data("S%sUTIL" % station)['average'][-1]
        print("station%s.value %s" % (station, util*100))
