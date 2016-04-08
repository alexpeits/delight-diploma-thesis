import time
#import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from numpy import clip, array
from numpy.polynomial import Polynomial
from ..config import *
#from ..config import (DIM_TABLE, GET_READ, GATEWAY_ADDR, DIM_MIN, DIM_MAX,
#                DIM_INCR_UP, DIM_INCR_DOWN, DIM_TO_VAL, THRESH_MIN, THRESH_MAX)
try:
    from colorize import clr_ret as clr
except ImportError:
    def clr(text, *args):
        return text


class Timer(object):
    def __init__(self, count):
        self.start = time.time()
        self.count = count

    def __call__(self):
        return time.time()-self.start <= self.count


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
        self.current_read = Light.thresh # most recent reading
        self.SEND_DELAY = SEND_DELAY

    def get_reading(self):
        """
        Request a reading from a sensor.
        The process is:
            send the request
            wait for response
            if a response is detected, store it
            else, if there is a timeout while waiting,
                continue with the previous stored value

        :rtype: int or None

        """
        time.sleep(self.SEND_DELAY)

        send_data = ''.join([self.addr, GET_READ, '        '])
        radio.write(send_data)

        timer = Timer(NODE_TIMEOUT)
        radio.startListening()
        while not radio.available(pipe, True) and timer():
            time.sleep(1000/1000000.0)
        recv_buffer = []
        radio.read(recv_buffer, radio.getDynamicPayloadSize())
        recv_data = ''.join(chr(i) for i in recv_buffer)
        radio.stopListening()

        dest = recv_data[:2]
        source = recv_data[2:4]
        #print 'Got packet: {}'.format(recv_data)
        if (source == self.addr) and (dest == GATEWAY_ADDR):
            self.current_read = int(recv_data[-4:])
            print clr('sensor {}, received {}'.format(self.addr, self.current_read),
                        'cyan')

    def __repr__(self):
        return '{}, addr {}'.format(self.__class__, self.addr)



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
        self._state = 'auto'
        self.intens = self.thresh
        self._sum = 0

    def dim_increment(self, dim, diff):
        """
        Dim by an increment. The increment is provided
        as a percent value, and it is modified to a
        value in dimmer units through multiplication by the
        mean_percentage value

        :type dim: integer
        :rtype: bool

        """
        times = self.make_mult(diff)
        incr_send = abs(int(times*self.mean_percentage*dim))
        if incr_send>MAX_INCR:
            incr_send = MAX_INCR
        if dim>0:
            send_data = ''.join([self.addr, DIM_INCR_UP, str((incr_send)), '       '])
        else:
            send_data = ''.join([self.addr, DIM_INCR_DOWN, str((incr_send)), '       '])
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

    def make_mult(self, diff):
        if diff < 30:
            return 1
        if diff < 60:
            return 2
        if diff < 90:
            return 4
        return 5

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

    def update_sum(self, val):
        self._sum += val
        abs_sum = abs(self._sum)
        if abs_sum>600 and self.state=='auto':
            self.state = 'nauto'
        elif abs_sum<=600 and self.state=='nauto':
            self.state = 'auto'
        self._sum = clip(self._sum, -600, 600)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, newstate):
        if self._state == 'nauto' and self._newstate != 'nauto':
            self._sum = 0
        self._state = newstate




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
    #power_recv = array([11, 22.5, 27.2, 31.33, 34.5, 37.3,
    #                    39.45, 41.35, 42.5, 45.35, 47])
    #power_expected = array([0, 4, 8, 12, 16,
    #                        20, 24, 28, 32, 36, 40])

    def __init__(self, addr, max_power, power_recv=None):
        Sensor.__init__(self, addr)
        power_expected = array([max_power*i/100 for i in xrange(0, 110, 10)])
        if power_recv is None:
            power_recv = power_expected[:]
        self._poly = Polynomial.fit(power_recv, power_expected, 2)
        #self.least_squares(power_recv, power_expected)
        self._conv = interp1d(*self._poly.linspace())
        self._min_recv = min(power_recv)
        self._max_recv = max(power_recv)
        self._min_pow = min(power_expected)
        self._max_pow = max(power_expected)
        self.recv_read = 0
        self.SEND_DELAY = 2

    def get_reading(self):
        Sensor.get_reading(self)
        print 'SCT reading:', self.current_read
        self.current_read = self.remove_error(self.current_read)

        print 'Converted to:', self.current_read

    def get_raw_reading(self):
        """
            For setup and testing purposes
            NOTE: also returns the current reading

        """
        Sensor.get_reading(self)
        return self.current_read

    def remove_error(self, p_recv):
        p_recv = p_recv/100.0
        p_recv_clipped = clip(p_recv, self._min_recv, self._max_recv)
        return clip(self._conv(p_recv_clipped), self._min_pow, self._max_pow)

    #def least_squares(self, p_rec, p_exp):
    #    plt.figure(figsize=(5*0.75, 5*0.75), dpi=96)
    #    plt.plot(*self._poly.linspace(), linewidth=1.2)
    #    plt.plot(p_rec, p_exp, 'ro', alpha=0.8)
    #    plt.title('$Sensor\,addr:\,{}$'.format(self.addr))
    #    plt.xlabel('$Measured\,power\,(W)$')
    #    plt.ylabel('$Expected\,power\,(W)$')
    #    plt.ylim(-5, 45)
    #    plt.grid(True)
    #    plt.tight_layout(True)
    #    plt.savefig('plot_{}.png'.format(self.addr), dpi=96)
