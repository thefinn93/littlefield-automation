#!/usr/bin/env python
import sys
import os
lib = os.getenv("LITTLEFIELD_PATH")
if lib is not None:
    sys.path.append(lib)
from littlefield import Littlefield

config = False
derive = "_derative" in sys.argv[0]
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True
if config:
    print("""graph_title Leaderboard
graph_info Shows the position on the leadership board
graph_category littlefield
graph_vlabel Cash ($)
""")

littlefield = Littlefield(os.getenv("LITTLEFIELD_USER"), os.getenv("LITTLEFIELD_PW"))
for team in littlefield.get_standings():
    if config:
        print("%s.label %s" % (team['name'], team['name']))
        if derative:
            print("%s.type DERIVE" % team['name'])
    else:
        print("%s.value %s" % (team['name'], team['cash']))
