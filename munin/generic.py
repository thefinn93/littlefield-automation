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

    def avg(data, size):
        return sum(data[((size*-1)-1):-1])/size

    titles = {
        "JOBIN": {"title": "Jobs accepted per day", "unit": "jobs"},
        "JOBQ": {"title": "Jobs waiting", "unit": "jobs"},
        "INV": {"title": "Inventory levels", "unit": "kits"},
        "JOBOUT": {"title": "Completed jobs", "unit": "jobs"},
        "JOBT": {"title": "Lead times", "unit": "Days"},
        "JOBREV": {"title": "Revenue", "unit": "Dollars ($)"},
        "S1Q": {"title": "Station 1 Queue Size", "unit": "Kits"},
        "S2Q": {"title": "Station 2 Queue Size", "unit": "Kits"},
        "S3Q": {"title": "Station 3 Queue Size", "unit": "Kits"},
        "S1UTIL": {"title": "Station 1 Utilitization", "unit": "Utilitization"},
        "S2UTIL": {"title": "Station 2 Utilitization", "unit": "Utilitization"},
        "S3UTIL": {"title": "Station 3 Utilitization", "unit": "Utilitization"}
    }

    if "_" in sys.argv[0]:
        name = sys.argv[0].split("_")[1]
    else:
        name = sys.argv[-1]

    config = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "config":
            config = True
    if config:
        print("graph_title %s" % titles[name]['title'])
        print("graph_info Shows the %s" % titles[name]['title'])
        print("graph_category littlefield")
        print("graph_vlabel %s" % titles[name]['unit'])

    littlefield = Littlefield(os.getenv("LITTLEFIELD_USER"), os.getenv("LITTLEFIELD_PW"))
    data = littlefield.get_data(name)
    if config:
        print("%s.label %s" % (name, titles[name]['title']))
        print("%s-3.label %s (3 day average)" % (name, titles[name]['title']))
        print("%s-10.label %s (10 day average)" % (name, titles[name]['title']))
    else:
        key = "average"
        print("%s.value %s" % (name, data[key][-1]))
        print("%s-3.value %s" % (name, avg(data[key], 3)))
        print("%s-10.value %s" % (name, avg(data[key], 10)))
except:
    raven.captureException()
