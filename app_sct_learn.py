from lights import *
from collections import defaultdict
import json, time

light_1 = Light('06')
light_2 = Light('07')

sct_1 = DissipationSensor(addr='08', max_power=40)
sct_2 = DissipationSensor(addr='09', max_power=40)

train_data = defaultdict(list)
assoc = {sct_1: light_1, sct_2: light_2}

for sct, light in assoc.items():
    for lum in xrange(0, 110, 10):
        light.dim_to_val(lum)
        time.sleep(4)
        reading = sct.get_raw_reading()
        train_data[sct.addr].append(reading/100.0)

with open('lights/sct_train_data.txt', 'w') as f:
    f.write(json.dumps(train_data))