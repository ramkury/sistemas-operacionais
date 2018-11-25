from collections import deque

# Extends 'deque' to implement simplified FIFO queue operations
class fifo_queue(deque):
	def put(self, elem):
		self.appendleft(elem)

	def get(self):
		return self.pop() if self else None

	def peek(self):
		return self[-1] if self else None

class ready_process_queue():
	def __init__(self):
		self.process_count = 0
		# Use only put() and get() methods on queues
		self.realtime_procs = fifo_queue()
		self.user_procs = [
			fifo_queue(), # Priority 1
			fifo_queue(), # Priority 2
			fifo_queue()  # Priority 3
		]
		self.all_procs = [self.realtime_procs, *self.user_procs]


	def print(self):
		print("%d processes ready." % self.process_count)
		print("Real time (priority 0): %d" % len(self.realtime_procs), end=" ")
		print([p.pid for p in self.realtime_procs])
		for i in range(3):
			print("User, priority %d: %d" % (i + 1, len(self.user_procs[i])), end=" ")
			print([p.pid for p in self.user_procs[i]])


	def put(self, process):
		self.all_procs[process.priority].put(process)
		self.process_count += 1


	def get(self):
		if self.process_count < 1:
			return None

		self.process_count -= 1
		for queue in self.all_procs:
			process = queue.get()
			if process:
				return process

	def has_processes(self):
		return any(self.all_procs)

