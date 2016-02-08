from RPi.GPIO import cleanup as GPIOcleanup
from scipy.interpolate import interp1d
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import re
from threading import Thread
import Queue
from numpy import clip

from lights import *


def close_all_lights():
    for light in Light.instances:
        light.dim_to_val(0)

def request_readings(sensor_type):
    for sensor in sensor_type.instances:
        sensor.get_reading()

def adjust_lights():
    thresh = Light.thresh
    cur_reads = [int(sensor.current_read) for sensor in LightSensor.instances]

    cur_reads = [thresh if abs(i-thresh)<=12 else i for i in cur_reads]
    for reading in cur_reads:
        if abs(reading-thresh)>30:
            Light.mean_percentage *= 2
            break
    else:
        Light.mean_percentage = abs(m_dim/10.0)

    states = [light.state for light in Light.instances]

    # If we have one light at auto and one at on or off, then
    # the send value for the auto light is calculated using a
    # weighted average.
    # ONLY IN CASE OF 2 LIGHT INSTANCES!
    #if 'auto' in states and ('on' in states or 'off' in states):
    #    send_val = 10.0*(2*thresh-sum(cur_reads))/sum([m_list[i][j] for i in xrange(len(LightSensor.instances)) for j in [0, 1]
    #                                                   if Light.instances[j].state=='auto'])
    #    send_vals = [send_val, send_val]
    if 'auto' in states and ('on' in states or 'off' in states):
        send_val = 10.0*(len(LightSensor.instances)*thresh-sum(cur_reads))/sum([m_list[i][j]
                                                                                for i in xrange(len(LightSensor.instances))
                                                                                for j in xrange(len(Light.instances))
                                                                                if Light.instances[j].state=='auto'])
        send_vals = [send_val, send_val]

    else:
        send_vals = get_next_dim(m_list, cur_reads, thresh)

    print send_vals
    for i, light in enumerate(Light.instances):
        if light.state=='auto':
            light.dim_increment(send_vals[i])

def init_lights():
    """
    Initial dimming to a value that results to the desired
    threshold. If the state from the conf file is 'on' or 'off',
    dim accordingly. If it is 'auto', dim to the closest multiple
    of 10, which is bigger than the calculated value.

    """
    from math import ceil

    v_send = get_next_dim(m_list,
                          [sensor.setup_table[0][0] for sensor in LightSensor.instances],
                          Light.thresh)
    print v_send
    for i, light in enumerate(Light.instances):
        if light.state=='on':
            light.dim_to_val(light.intens)
        elif light.state == 'off':
            light.dim_to_val(0)
        else:
            intens = 10*ceil(v_send[i]/10.0)
            light.dim_to_val(clip(int(intens), 0, 100))

def _db_insert(sct):
    db_insert(int(sct.addr), sct.current_read)

def _mqtt_publish(sct):
    mqtt_publish(sct.addr, sct.current_read)

class GUIDataChangeHandler(FileSystemEventHandler):
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
                Light.mapping.get(key[6:8]).intens = int(val) if val is not None else 50
        # queue any dimming tasks, if necessary
        for light in Light.instances:
            state = ''.join(['light_', light.addr, '_state'])
            intens = ''.join(['light_', light.addr, '_int'])

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
            self._execute(task)
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
sct_1 = DissipationSensor('08')

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

init_lights()

queue = Queue.Queue()

handler = CommHandler(queue)
handler.setDaemon(True)

gui_data_handler = GUIDataChangeHandler(queue)
observer = Observer()
observer.schedule(gui_data_handler, "/var/www/data", recursive=False)

handler.start()
observer.start()

try:
    while True:
        task = [request_readings, [LightSensor]]
        queue.put(task)

        task = [adjust_lights, []]
        queue.put(task)

        task = [request_readings, [DissipationSensor]]
        queue.put(task)

        for sct in DissipationSensor.instances:
            task = [_db_insert, [sct]]
            queue.put(task)
            task = [_mqtt_publish, [sct]]
            queue.put(task)

        time.sleep(15)

except KeyboardInterrupt:
    print 'Wait for all tasks to be completed...'
    queue.join()
    prompt = raw_input('Close all lights? [y/n] ')
    if prompt == 'y':
        close_all_lights()

    cur.close()
    db.close()
    mqttc.disconnect()
    GPIOcleanup()
    print 'EXITING'
