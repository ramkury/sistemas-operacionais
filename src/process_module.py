from queue_module import ready_process_queue, fifo_queue
import memory_module as memory
class process():
	_pid = 0

	def __init__(self, proc_info):
		info_str = proc_info.split(',')
		if len(info_str) != 8:
			raise BaseException("Bad input file")
		info = [int(s) for s in info_str]
		self.pid = process._pid
		self.offset = -1
		self.startup_time = info[0] #
		self.priority     = info[1] # lower number = higher priority
		self.proc_time    = info[2] #
		self.mem_blocks   = info[3] #
		self.printer      = info[4] # 0 means a printer was not required
		self.scanner      = info[5] # 0 means a scanner was not required
		self.modem        = info[6] # 0 means the modem was not required
		self.disk         = info[7] # 0 means the disk was not required
		self._instruction = 0
		process._pid += 1

	def run(self):
		if self._instruction == 0:
			print("Process %d STARTED" % self.pid)
		
		self._instruction += 1
		print("Process %d: instruction %d" % (self.pid, self._instruction))		

		if self._instruction < self.proc_time:
			return False
		else:
			print("Process %d: return SIGINT" % self.pid)
			return True

class process_manager():
	def __init__(self):
		self.ready_queue = ready_process_queue()
		self.running = self.ready_queue.get()
		
	def run(self):
		if not self.running:
			self.running = self.ready_queue.get()
			if not self.running:
				return False

		completed = self.running.run()

		if completed:
			# If process is finished, free its resources
			self._free_resources(self.running)
			self.running = self.ready_queue.get()
		
		elif self.running.priority > 0:
			if self.running.priority < 3:
				# If it is not lowest priority, lower the process's priority
				self.running.priority += 1

			self.ready_queue.put(self.running)
			self.running = self.ready_queue.get()

		return True


	def add_process(self, process):
		address = memory.check_mem(process.priority, process.mem_blocks)
		if address is None:
			return False
		process.offset = address
		self.ready_queue.put(process)


	def has_processes(self):
		return self.ready_queue.has_processes()


	def _free_resources(self, process):
		memory.check_free_mem(process.offset, process.mem_blocks, process.priority)