from queue_module import fifo_queue

class dispatcher():
	def __init__(self, processes):
		self.process_queue = fifo_queue()
		self.process_queue.extend(sorted(processes, lambda p: p.startup_time))
		
	def dispatch(self, process):
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
		
	
		