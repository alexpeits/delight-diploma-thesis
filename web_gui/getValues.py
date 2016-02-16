#!/usr/bin/env python
import cgi, cgitb
import json

cgitb.enable(logdir="/var/www/logs", display=False, format="text")
form = cgi.FieldStorage(keep_blank_values=0)

conf_write = {}
conf_write['thresh'] = form.getvalue('thresh')
conf_write['light_06_state'] = form.getvalue('light_06_state')
conf_write['light_06_int'] = form.getvalue('light_06_int')
conf_write['light_07_state'] = form.getvalue('light_07_state')
conf_write['light_07_int'] = form.getvalue('light_07_int')


with open('/var/www/data/gui.conf', 'r') as f:
	conf_read_json = f.read()

conf_read = json.loads(conf_read_json)


if conf_write != conf_read:
	conf_write_json = json.dumps(conf_write)
	with open('/var/www/data/gui.conf', 'w') as f:
		f.write(conf_write_json)


print "Content-type:text/html\n"
