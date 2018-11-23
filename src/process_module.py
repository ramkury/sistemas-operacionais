from queue_module import ready_process_queue, fifo_queue

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
		print("Process %d" % self.pid)
		if self._instruction == 0:
			print("\tSTARTED")
		else:
			print("\tRESUMED")
		
		if self.priority == 0:
			for _ in range(self.proc_time):
				self._run_instruction()
		else:
			self._run_instruction()
		
		if self._instruction < self.proc_time:
			print("\tBLOCKED")
			return False
		else:
			print("\treturn SIGINT")
			return True

	def _run_instruction(self):
		self._instruction += 1
		print("\tinstruction %d" % self._instruction)

class process_manager():
	def __init__(self, processes):
		self.ready_queue = ready_process_queue()
		for process in processes:
			self.ready_queue.put(process)
		self.running = self.ready_queue.get()
		self.current_time = 0
		
	def run(self):
		if self.running.run():
			# If process is finished, free its resources
			self.free_resources()
		
		else:
			if self.running.priority < 3:
				# If it is not lowest priority, lower the process's priority
				self.running.priority += 1
			self.ready_queue.put(self.running)

		return self.dispatch(self.ready_queue.get())


	def dispatch(self, process):
		self.running = process
		if not process:
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

	def _increment_time(self, process):
		if self.running.priority == 0:
			self.current_time += self.running.proc_time
		else:
			self.current_time += 1

	def free_resources(self):
		pass

	def update_processes(self):
		pass