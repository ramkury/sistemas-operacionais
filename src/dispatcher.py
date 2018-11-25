from queue_module import fifo_queue

class dispatcher():
	def __init__(self, processes):
		self.current_time = -1
		self.process_queue = fifo_queue()
		self.process_queue.extend(sorted(processes, key = lambda p: p.startup_time, reverse = True))
		
	def dispatch(self, process):
		print("Dispatcher =>")
		print("\tPID: %d" % process.pid)
		
		if process.offset < 0:
			print("\tNão há memória suficiente para o processo")
			return

		print("\toffset: %d" % process.offset)
		print("\tblocks: %d" % process.mem_blocks)
		print("\tpriority: %d" % process.priority)
		print("\ttime: %d" % process.proc_time)
		print("\tprinter: %d" % process.printer)
		print("\tscanner: %d" % process.scanner)
		print("\tmodem: %d" % process.modem)
		print("\tdrive: %d" % process.disk)
		
	
	def run(self, manager):
		self.current_time += 1
		while self.process_queue and self.process_queue.peek().startup_time == self.current_time:
			process = self.process_queue.get()
			manager.add_process(process)
			self.dispatch(process)
	
	def has_processes(self):
		return any(self.process_queue)