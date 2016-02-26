#!/usr/bin/env python
import sys
import os
lib = os.getenv("LITTLEFIELD_PATH")
if lib is not None:
    sys.path.append(lib)
from littlefield import Littlefield
from raven import Client
raven = Client(os.getenv("LITTLEFIELD_RAVEN_DSN"))
try:
    config = False
    derive = "_derative" in sys.argv[0]
    if len(sys.argv) > 1:
        if sys.argv[1] == "config":
            config = True
    if config:
        title = "Cash Levels by Team" if not derive else "Cash delta by Team"
        print("""graph_title %s
graph_info Shows the position on the leadership board
graph_category littlefield
graph_vlabel Cash ($)""" % title)
        if derive:
            print("graph_args --upper-limit 5 --lower-limit 0")
            print("graph_scale no")

    littlefield = Littlefield(os.getenv("LITTLEFIELD_USER"), os.getenv("LITTLEFIELD_PW"))
    for team in littlefield.get_standings():
        if config:
            print("%s.label %s" % (team['name'], team['name']))
            if derive:
                print("%s.type DERIVE" % team['name'])
        else:
            print("%s.value %s" % (team['name'], team['cash']))
except:
    raven.captureException()
