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
        print("graph_title Cash Uses")
        print("graph_info Shows the various sources and uses of cash")
        print("graph_category littlefield")
        print("graph_vlabel Dollars ($)")
        print("machines.label machines")
        print("machines.draw AREA")
        print("inventory.label inventory")
        print("inventory.draw STACK")

    else:
        littlefield = Littlefield(os.getenv("LITTLEFIELD_USER"), os.getenv("LITTLEFIELD_PW"))
        data = littlefield.get_cash()
        print("machines.value %s" % data['machines'])
        print("inventory.value %s" % data['inventory'])
except:
    raven.captureException()
