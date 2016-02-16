#!/usr/bin/env python
import json

init_values_temp = []

with open("/var/www/data/gui.conf", "r") as f:
	conf_read_json = f.read()

conf_read = json.loads(conf_read_json)
init_values_temp.append(conf_read['thresh'])
init_values_temp.append(conf_read['light_06_state'])
init_values_temp.append(conf_read['light_06_int'])
init_values_temp.append(conf_read['light_07_state'])
init_values_temp.append(conf_read['light_07_int'])
init_values = [i if i is not None else '0' for i in init_values_temp]

init_values = "/".join(init_values) + "/"

print "Content-type:text/html\n"
print "%s" % (init_values)
