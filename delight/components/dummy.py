"""
Dummy components to be used in testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Components defined here abstract away hardware calls or
other calls that should not be used in testing.

"""

import time


class DummyObject(object):
    """Provide dummy behavior for calling."""

    def __call__(self, *args, **kwargs):
        return None


class DummyRadio(object):
    """Dummy implementation of RF radio.

    Provides some basic methods to simulate sending
    and receiving. Other methods not useful in testing
    return a DummyObject instance, that can be called
    or assigned (returning None either way).
    """

    WRITE_TIME = 0.2
    READ_TIME = 0.2
    WAIT_AVAIL_TIME = 0.2

    def __init__(self, *args, **kwargs):
        super(DummyRadio, self).__init__()

    def write(self, *args, **kwargs):
        time.sleep(self.WRITE_TIME)
        return True

    def read(self, *args, **kwargs):
        time.sleep(self.READ_TIME)
        return 'TODO'

    def available(self, *args, **kwargs):
        time.sleep(self.WAIT_AVAIL_TIME)
        return True

    def __getattr__(self, attr):
        return DummyObject()
