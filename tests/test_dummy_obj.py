"""Dummy objects test module.

Used to test classes defined in delight/components/dummy

"""

import unittest
import time

from delight.components.dummy import DummyRadio


class TestDummyRadio(unittest.TestCase):
    """Tests for the 'patched' NRF24 class."""

    def setUp(self):
        self.radio = DummyRadio()

    def test_write(self):
        start = time.time()
        self.assertTrue(self.radio.write())
        dt = time.time() - start
        self.assertGreater(dt, self.radio.WRITE_TIME)
        self.assertTrue(self.radio.write(1, 2, 'arg'))
        self.assertTrue(self.radio.write(1, 2, 'arg', kw='foo'))

    def test_read(self):
        start = time.time()
        self.assertTrue(self.radio.read())
        dt = time.time() - start
        self.assertGreater(dt, self.radio.READ_TIME)
        self.assertTrue(self.radio.read(1, 2, 'arg'))
        self.assertTrue(self.radio.read(1, 2, 'arg', kw='foo'))

    def test_available(self):
        start = time.time()
        self.assertTrue(self.radio.available())
        dt = time.time() - start
        self.assertGreater(dt, self.radio.WAIT_AVAIL_TIME)
        self.assertTrue(self.radio.available(1, 2, 'arg'))
        self.assertTrue(self.radio.available(1, 2, 'arg', kw='foo'))


if __name__ == '__main__':
    unittest.main()
