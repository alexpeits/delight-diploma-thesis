"""
Abstract hardware classes
~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from delight.components.mixins import NRFMixin


class Sensor(NRFMixin):
    """Abstract class for a sensor that can communicate through an NRF"""

    def __init__(self, radio, pipe, addr):
        self.radio = radio
        self.pipe = pipe
        self.addr = addr

    def read(self):
        pass
