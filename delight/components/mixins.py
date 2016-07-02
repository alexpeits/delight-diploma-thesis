"""
Class mixins to provide functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import time

from delight.config import GW_ADDR


class NRFMixin(object):
    """Mixin for a class that sends and receives through an NRF24L01."""

    def send(self, data):
        time.sleep(self.SEND_DELAY)
        self.radio.write(data)

    def recv(self):
        self.radio.startListening()
        while not self.radio.available(self.pipe, True):
            time.sleep(self.RECV_DELAY)
        recv_buffer = []
        self.radio.read(recv_buffer, self.radio.getDynamicPayloadSize())
        self.radio.stopListening()
        data = ''.join(map(chr, recv_buffer))
        return data


class AddressableDevice(object):
    """Mixin for handling devices with addresses.

    Provides functionality for creating the payload prior to
    sending it, and validating an incoming payload.

    """

    def create_payload(self, command=None, data=None):
        """Wrap the data to be sent with the appropriate headers.

        The payload has the following form:

        |-------------+-----------+---------+---------|
        | source addr | dest addr | command | data    |
        |-------------+-----------+---------+---------|
        | 2 bytes     | 2 bytes   | 2 bytes | 4 bytes |
        |-------------+-----------+---------+---------|

        """
        pass
