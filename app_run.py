from RPi.GPIO import cleanup as GPIOcleanup
from scipy.interpolate import interp1d
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import re
from threading import Thread
import Queue

from lights import *


def close_all_lights():
    for light in Light.instances:
        light.dim_to_val(0)

def request_readings(sensor_type):
    for sensor in sensor_type.instances:
        sensor.get_reading()

def adjust_lights(send_vals=None):
    if send_vals==None:
        return
    for i, light in enumerate(Light.instances):
        if light.state=='auto':
            light.dim_increment(send_vals[i])


class GUIDataChangeHandler(FileSystemEventHandler):
    """
    This class handles the execution of commands from
    the WebGUI. Upon the change of the conf file, the
    'on_modified' method is called.

    """
    def __init__(self, queue):
        FileSystemEventHandler.__init__(self)
        self.queue = queue

    def on_modified(self, event):
        """
        the json file has the following format:
        {'light_xy_state': 'on' or 'off' or 'auto',
         'light_xy_int'  : '0' or '10' .... or '100',
         .
         .
         'thresh'        : '0' to '800'
        }

        """
        global gui_data
        with open(GUI_CONF_PATH, 'r') as f:
            gui_new = json.loads(f.read())
        # update light instance and class attributes
        for key, val in gui_new.items():
            if key=='thresh':
                Light.thresh = int(val)
            elif key[9:]=='state':
                Light.mapping.get(key[6:8]).state = val
            elif key[9:]=='int':
                Light.mapping.get(key[6:8]).intens = val
        # queue any dimming tasks, if necessary
        for light in Light.instances:
            state = ''.join['light_', light.addr, '_state']
            intens = ''.join['light_', light.addr, '_int']

            if gui_new.get(state) == 'auto':
                continue
            if gui_new.get(state) == 'off' and gui_new.get(state) != gui_data.get(state):
                task = [light.dim_to_val, [0]]
                self.queue.put(task)
                continue
            if gui_new.get(state) != gui_data.get(state) or gui_new.get(intens) != gui_data.get(intens):
                task = [light.dim_to_val, [light.intens]]
                self.queue.put(task)

        gui_data = gui_new


class CommHandler(Thread):
    """
    This class handles all communications during the
    regular stage of the system. It runs in a dedicated
    thread, and monitors the global queue. When there is
    a task to be executed, it calls the passed function
    with the arguments provided.

    """
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            task = self.queue.get()
            _execute(task)
            self.queue.task_done()

    def _execute(self, task):
        """
        A task is a list, formatted like this:
        [callable, [args]]

        The [args] list can have any length, and
        it doesn't matter, since we use the star (*)
        to unpack it.

        """
        task[0](*task[1])


# instantiate with an address
light_1 = Light('06')
light_2 = Light('07')
lsensor_1 = LightSensor('04')
lsensor_2 = LightSensor('03')

#TODO: arg parsing
setup_from_file()
gui_data = read_init_data()
thresh = int(gui_data.get('thresh'))

v_list = [[] for i in LightSensor.instances]
for i, sensor in enumerate(LightSensor.instances):
    v_list[i] = sensor.setup_table

d_list = [[] for i in LightSensor.instances]
for i, sublist in enumerate(v_list):
    d_list[i] = get_diff(sublist)

m_list = [[] for i in LightSensor.instances]
for i, sublist in enumerate(d_list):
    m_list[i] = get_mean(sublist)

v_dim = [int(i) for i in DIM_TABLE]
d_dim = [v_dim[i+1] - v_dim[i] for i in xrange(len(v_dim)-1)]
m_dim = sum(d_dim)/len(d_dim)
Light.mean_percentage = abs(m_dim/10.0)

recv_reads = [thresh, thresh] # storage for sensor readings
print 'v_list: {}'.format(v_list)
print 'd_list: {}'.format(d_list)
print 'm_list: {}'.format(m_list)
print 'd_dim: {}'.format(d_dim)
print 'm_dim: {}'.format(m_dim)
print gui_data

#based on thresh, find the initial light intensity
v_send = get_next_dim(m_list, [sensor.setup_table[0][0] for sensor in LightSensor.instances], thresh)

print 'DEBUG', v_send
for i, val in enumerate(v_send):
    for j, dim in enumerate(DIM_TABLE):
        if val<j*10:
            flag = j
            break
	conv = interp1d([(flag-1)*10, flag*10], [DIM_TABLE[j-1], DIM_TABLE[j]])
	v_send[i] = int(conv(v_send[i]))

print 'INITIAL', v_send
for i, light in enumerate(Light.instances):
    light.dim_real_value(v_send[i])


queue = Queue.Queue(1) # With size 1, queue acts as a lock
gui_data_handler = GUIDataChangeHandler()
observer = Observer()
observer.schedule(gui_data_handler, GUI_CONF_PATH, recursive=False)
observer.start()

try:
    while True:
        task = [request_readings, [LightSensor]]
        queue.put(task)
        cur_reads = [sensor.current_read for sensor in LightSensor.instances]

        #task = [request_readings, [DissipationSensor]]
        #queue.put(task)

        cur_reads = [thresh if abs(i-thresh)<=12 else i for i in cur_reads]
        for reading in cur_reads:
            if abs(reading-thresh)>30:
                Light.mean_percentage *= 2
                break
        else:
            Light.mean_percentage = abs(m_dim/10.0)

        send_next = get_next_dim(m_list, cur_reads, Light.thresh)
        print cur_reads
        print send_next

        task = [adjust_lights, [send_next]]
        queue.put(task)

        time.sleep(5)

except KeyboardInterrupt:
    prompt = raw_input('Close all lights? [y/n] ')
    if prompt == 'y':
        close_all_lights()

    cur.close()
    db.close()
    mqttc.disconnect()
    GPIOcleanup()
    print 'KEYBOARD INTERRUPT'
