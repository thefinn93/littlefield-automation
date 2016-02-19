#!/usr/bin/env python
from littlefield import Littlefield
from configparser import ConfigParser

config = ConfigParser()
config.read(['littlefield.ini'])

littlefield = Littlefield(config['littlefield']['user'], config['littlefield']['password'])
i = 1
for team in littlefield.get_standings():
    print("%s. %s ($%s)" % (i, team['name'], team['cash']))
    i += 1
