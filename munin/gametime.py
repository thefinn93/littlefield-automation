#!/usr/bin/env python
import sys
import os
lib = os.getenv("LITTLEFIELD_PATH")
if lib is not None:
    sys.path.append(lib)
from raven import Client
raven = Client(os.getenv("LITTLEFIELD_RAVEN_DSN"))
try:
    from littlefield import Littlefield

    config = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "config":
            config = True
    if config:
        print("graph_title Game Time")
        print("graph_info Shows the number of game days that have passed")
        print("graph_category littlefield")
        print("graph_vlabel days")

    littlefield = Littlefield(os.getenv("LITTLEFIELD_USER"), os.getenv("LITTLEFIELD_PW"))
    if config:
        print("days.label Game Days")
    else:
        key = None
        data = littlefield.get_status()
        print("days.value %s" % status['day'])
except:
    raven.captureException()
