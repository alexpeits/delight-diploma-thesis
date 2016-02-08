import json
import time
from .config import *
from .components.devices import *


def read_init_data():
    """
    Read the current data provided by the web interface,
    store them accordingly and return a dict with references
    to each instance or class attribute

    :rtype: dict

    """
    with open(GUI_CONF_PATH, 'r') as f:
        init_data_json = f.read()
    init_data = json.loads(init_data_json)

    gui_data = init_data

    for key, val in init_data.items():
        if key=='thresh':
            gui_data[key] = Light.thresh = int(val)
        elif key[9:]=='state':
            gui_data[key] = Light.mapping.get(key[6:8]).state = val
        elif key[9:]=='int':
            gui_data[key] = Light.mapping.get(key[6:8]).intens = int(val) if val is not None else 50

    return gui_data

def setup():
    """
    For each light that has been instantiated, increment its
    intensity level by 10% (the next value in DIM_TABLE), while
    each other light is at 0%. For each incrementation, request
    a reading from each of the LightSensors that have been
    instantiated, and store it to its setup_table (the index
    depends on the Light instance). Finally, store each sensor
    setup_table in a file in JSON format.

    """
    for bulb_i, bulb in enumerate(Light.instances):
        for b in Light.instances:
            b.dim_to_val(0)
        for i in xrange(len(DIM_TABLE)):
            bulb.dim_to_val(i*10)
            for sensor in LightSensor.instances:
                sensor.get_reading()
                reading = sensor.current_read
                print reading
                sensor.setup_table[bulb_i].append(reading)
                print sensor.setup_table

    config = {}
    for i, sensor in enumerate(LightSensor.instances):
        config[sensor.addr] = sensor.setup_table
    config_json = json.dumps(config)
    print config

    with open(CONFIGPATH, 'w') as f:
        f.write(config_json)

def setup_from_file():
    """
    Instead of setting up the system from scratch, it can
    be set up by a previous saved configuration. This conf
    is stored in each LightSensor's setup_table.

    """
    with open(CONFIGPATH, 'r') as f:
        config_json = f.read()
    config = json.loads(config_json)

    for key in config:
        try:
            LightSensor.mapping.get(key).setup_table = config[key]
        except KeyError:
            raise KeyError('Invalid config file')
