"""
Inter-process communication utilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from multiprocessing.connection import Client, Listener
from threading import import Thread

# TODO: auth key

AUTH_KEY = None


class AsyncListener(Thread):
    """Non-blocking version of Listener

    Not actually async, because it runs in a separate thread.
    When there is a task to be executed, AsyncListener pushes
    it in a queue. The task is then executed by the main
    worker. Kinda like an event loop, but not really.
    """

    def __init__(self, address, queue):
        super(AsyncListener, self).__init__()
        self.setDaemon(True)
        self.server = Listener(address, authkey=AUTH_KEY)
        self.queue = queue

    def run(self):
        self.client_conn = self.server.accept()
        while True:
            msg = self.client_conn.recv()
            self.handle(msg)

    def handle(self, msg):
        self.queue.push(msg)
