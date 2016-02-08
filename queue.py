class Queue(object):
	"""
	A basic FIFO queue to supplement
	the automated lights system.

	"""

	def __init__(self):
		self.container = []
		
	def size(self):
		return len(self.container)

	def enqueue(self, item):
		self.container.insert(0, item)

	def dequeue(self):
		try:
			return self.container.pop()
		except IndexError:
			return None

	def is_empty(self):
		return len(self.container) == 0

	def next(self):
		try:
			return self.container[-1]
		except IndexError:
			return None