"""
Class mixins to provide functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""


class Transmitter(object):
    """Mixin representing a device that can send data."""

    def send(self, data):
        raise NotImplementedError()


class Receiver(object):
    """Mixin representing a device that can receive data."""

    def recv(self, data):
        raise NotImplementedError()


class Transceiver(Transmitter, Receiver):
    """Mixin representing a class that can send and receive."""
    pass
