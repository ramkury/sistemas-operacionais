from collections import deque

# Extends `deque` to implement simplified FIFO queue operations
class fifo_queue(deque):
	def put(self, elem):
		self.appendleft(elem)

	def get(self):
		return self.pop()


class ready_process_queue():
	max_procs = 1000
	def __init__(self):
		self.process_count = 0
		self.realtime_procs = fifo_queue()
		self.user_procs = [
			fifo_queue(), # Priority 1
			fifo_queue(), # Priority 2
			fifo_queue()  # Priority 3
		]


	def print(self):
		print("%d processes ready." % self.process_count,)
		print("Real time (priority 0): %d" % len(self.realtime_procs), end=" ")
		print([p.pid for p in self.realtime_procs])
		for i in range(3):
			print("User, priority %d: %d" % (i + 1, len(self.user_procs[i])), end=" ")
			print([p.pid for p in self.user_procs[i]])


	def put(self, process):
		if process.priority == 0:
			self.realtime_procs.put(process)
		else:
			self.user_procs[process.priority - 1].put(process)
		self.process_count += 1


	def get(self):
		if self.process_count < 1:
			return None
		self.process_count -= 1
		if len(self.realtime_procs) > 0:
			return self.realtime_procs.get()
		for q in self.user_procs:
			if len(q) > 0:
				return q.get()

