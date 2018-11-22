from queue_module import ready_process_queue

class process():
	_pid = 0

	def __init__(self, proc_info):
		info_str = proc_info.split(',')
		if len(info_str) != 8:
			raise BaseException("Bad input file")
		info = [int(s.replace(' ', '')) for s in info_str]
		self.pid = process._pid
		self.offset = 0
		self.startup_time = info[0] #
		self.priority     = info[1] # lower number = higher priority
		self.proc_time    = info[2] #
		self.mem_blocks   = info[3] #
		self.printer      = info[4] # 0 means a printer was not required
		self.scanner      = info[5] # 0 means a scanner was not required
		self.modem        = info[6] # 0 means the modem was not required
		self.disk         = info[7] # 0 means the disk was not required
		process._pid += 1

class dispatcher():
	_quantum = 1 # in seconds

	def __init__(self, processes):
		self.ready_queue = ready_process_queue()
		self.blocked = []
		for process in processes:
			self.ready_queue.put(process)
		self.running = self.ready_queue.get()
		
	def run(self):
		self.running.proc_time -= dispatcher._quantum
		if self.running.proc_time <= 0:
			# Process is finished, release memory and resources
			return self.dispatch(self.ready_queue.get())
		
		if self.running.priority == 0: # Do not preempt real-time processes
			self.dispatch(self.running)
			return True

		if self.running.priority < 3:
			self.running.priority += 1

		self.ready_queue.put(self.running)
		self.dispatch(self.ready_queue.get())


	def dispatch(self, process):
		self.running = process
		if process is None:
			return False
		print("Dispatcher =>")
		print("\tPID: %d" % process.pid)
		print("\toffset: %d" % process.offset)
		print("\tblocks: %d" % process.mem_blocks)
		print("\tpriority: %d" % process.priority)
		print("\ttime: %d" % process.proc_time)
		print("\tprinter: %d" % process.printer)
		print("\tscanner: %d" % process.scanner)
		print("\tmodem: %d" % process.modem)
		print("\tdrive: 0%d" % process.disk)
		return True
