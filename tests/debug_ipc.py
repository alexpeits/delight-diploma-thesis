import sys; sys.path.append('./'); sys.path.append('../')

from Queue import Queue

from delight.utils.ipc import AsyncListener


class TestListener(AsyncListener):

    def handle(self, msg):
        self.queue.put(msg)
        print self.queue.get()


q = Queue()
server = TestListener(q)
server.start()
server.join()
print 'EXITING SERVER'
