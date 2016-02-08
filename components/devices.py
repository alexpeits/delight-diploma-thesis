import time
from scipy.interpolate import interp1d
from numpy import clip, array
from numpy.polynomial import Polynomial
from ..config import *
#from ..config import (DIM_TABLE, GET_READ, GATEWAY_ADDR, DIM_MIN, DIM_MAX,
#                DIM_INCR_UP, DIM_INCR_DOWN, DIM_TO_VAL, THRESH_MIN, THRESH_MAX)


class Sensor(object):
    """
    Base class for all types of sensors. It implements a
    method to request a reading from a sensor.

    """
    def __init__(self, addr):
        self.addr = addr
        self.instances.append(self)
        self.mapping[addr] = self
        # setup_table length equal to no. of lights
        self.setup_table = [[] for _ in xrange(len(Light.instances))]
        self.current_read = None # most recent reading

    def get_reading(self):
        """
        Request a reading from a sensor.

        :rtype: int or None

        """
        time.sleep(SEND_DELAY)

        send_data = ''.join([self.addr, GET_READ, '        '])
        radio.write(send_data)

        radio.startListening()
        while not radio.available(pipe, True):
            time.sleep(1000/1000000.0)
        recv_buffer = []
        radio.read(recv_buffer, radio.getDynamicPayloadSize())
        recv_data = ''.join(chr(i) for i in recv_buffer)
        radio.stopListening()

        dest = recv_data[:2]
        source = recv_data[2:4]
        print 'Got packet: {}'.format(recv_data)
        if (source == self.addr) and (dest == GATEWAY_ADDR):
            self.current_read = int(recv_data[-4:])


class Light(object):
    """
    Class for all lights. It implements a method to dim by an increment,
    and another one to dim to a specific DIM_TABLE value (only used in the
    setup stage). It also keeps track of every Light instance, in the
    instances table.

    """
    instances = []
    mapping = {}
    mean_percentage = None
    thresh = THRESH_MAX

    def __init__(self, addr):
        self.addr = addr
        self.instances.append(self)
        self.mapping[addr] = self
        self.state = 'auto'
        self.intens = self.thresh

    def dim_increment(self, dim):
        """
        Dim by an increment. The increment is provided
        as a percent value, and it is modified to a
        value in dimmer units through multiplication by the
        mean_percentage value

        :type dim: integer
        :rtype: bool

        """
        incr_send = int(self.mean_percentage*dim)
        if dim>0:
            send_data = ''.join([self.addr, DIM_INCR_UP, str(abs(dim)), '       '])
        else:
            send_data = ''.join([self.addr, DIM_INCR_DOWN, str(abs(dim)), '       '])
        time.sleep(SEND_DELAY)
        radio.write(send_data)

    def dim_to_val(self, val):
        """
        Dim to a value (0-100%)

        :type val: integer
        :rtype: bool
        """
        send_data = ''.join([self.addr, DIM_TO_VAL,
                        DIM_TABLE[val/10], '       '])
        time.sleep(SEND_DELAY)
        radio.write(send_data)
        #print 'Light {} to value {}%'.format(self.addr, val)

    def dim_real_value(self, val):
        """
        Dim to a value (DIM_MIN-DIM_MAX)

        :type val: integer
        :rtype: bool
        """
        val = clip(val, DIM_MIN, DIM_MAX)
        send_data = ''.join([self.addr, DIM_TO_VAL,
                        str(val), '       '])
        time.sleep(SEND_DELAY)
        radio.write(send_data)
        #print 'Light {} to value {}%'.format(self.addr, val)



class LightSensor(Sensor):
    """
    Inherits from the Sensor class. Here, we use the 'instances'
    table to keep track of all instances of this class. This way
    we can request readings simply by iterating through this table,
    and invoking LightSensor.instances[i].get_reading()

    """
    instances = []
    mapping = {}


class DissipationSensor(Sensor):
    """
    Inherits from the Sensor class. Here, we use the 'instances'
    table to keep track of all instances of this class. This way
    we can request readings simply by iterating through this table,
    and invoking DissipationSensor.instances[i].get_reading()

    """
    instances = []
    mapping = {}
    #power_recv = array([2.6, 16.4, 20.9, 24.6, 26.7,
    #                    29.5, 32, 33.85, 35.5, 36.5, 42])
    power_recv = array([11, 22.5, 27.2, 31.33, 34.5, 37.3,
                        39.45, 41.35, 42.5, 45.35, 47])
    power_expected = array([0, 4, 8, 12, 16,
                            20, 24, 28, 32, 36, 40])

    def __init__(self, addr):
        Sensor.__init__(self, addr)
        self._poly = Polynomial.fit(self.power_recv, self.power_expected, 2)
        self._conv = interp1d(*self._poly.linspace())

    def get_reading(self):
        Sensor.get_reading(self)
        print self.current_read, 'received'
        self.current_read = self.remove_error(self.current_read)
        print self.current_read, 'converted'

    def remove_error(self, p_recv):
        p_recv = p_recv/100.0
        p_recv_clipped = clip(p_recv, 11, 47)
        return clip(self._conv(p_recv_clipped), 0, 40)
