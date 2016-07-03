"""
Inter-process communication utilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from multiprocessing.connection import Client, Listener
from threading import Thread

from delight.config import DL_HOST, DL_PORT, DL_AUTH_KEY


class AsyncListener(Thread):
    """Non-blocking version of Listener

    Not actually async, because it runs in a separate thread.
    When there is a task to be executed, AsyncListener pushes
    it in a queue. The task is then executed by the main
    worker. Kinda like an event loop, but not really.

    """

    def __init__(self, queue, host=DL_HOST, port=DL_PORT):
        super(AsyncListener, self).__init__()
        self.setDaemon(True)
        address = (host, port)
        self.server = Listener(address, authkey=DL_AUTH_KEY)
        self.queue = queue

    def run(self):
        while True:
            self.client = self.server.accept()
            msg = self.client.recv()
            if msg == 'exit':  # temporary
                break
            self.handle(msg)

    def handle(self, msg):
        self.queue.put(msg)


def send(data, host=DL_HOST, port=DL_PORT, authkey=DL_AUTH_KEY):
    """Connect to a port on the host, send data and disconnect."""
    address = (host, port)
    client = Client(address, authkey=authkey)
    client.send(data)
    client.close()
