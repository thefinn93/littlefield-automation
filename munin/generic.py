#!/usr/bin/env python
import sys
import os
lib = os.getenv("LITTLEFIELD_PATH")
if lib is not None:
    sys.path.append(lib)
from littlefield import Littlefield


titles = {
    "JOBIN": {"title": "Number of jobs accepted per day", "unit": "jobs"},
    "JOBQ": {"title": "Number of jobs waiting", "unit": "jobs"},
    "INV": {"title": "Inventory levels", "unit": "kits"},
    "JOBOUT": {"jobs": "Number of completed jobs", "unit": "jobs"},
    "JOBT": {"title": "Lead times", "time"},
    "JOBREV": {"title": "Revenue", "unit": "Dollars ($)"},
}

name = sys.argv[0].split("_")[1]

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
if config:
    print("%s.label %s" % (name, titles[name]['title']))
else:
    key = None
    data = littlefield.get_data(name)
    for k in data.keys():
        if k != "days":
            key = k
    print("station%s.value %s" % (name, data[key][-1]))
