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
        print("graph_title Cash")
        print("graph_info Shows the various sources and uses of cash")
        print("graph_category littlefield")
        print("graph_vlabel $")

    littlefield = Littlefield(os.getenv("LITTLEFIELD_USER"), os.getenv("LITTLEFIELD_PW"))
    data = littlefield.get_cash()

    for key, value in data.items():
        if config:
            print("%s.label %s" % (key, key))
            print("%s.draw STACK")
        else:
            print("%s.value %s" % (key, value))
except:
    raven.captureException()
