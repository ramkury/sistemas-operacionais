class process():
	_pid = 0

	def __init__(self, proc_info):
		info_str = proc_info.split(',')
		if len(info_str) != 8:
			raise BaseException("Bad input file")
		info = [int(s.replace(' ', '')) for s in info_str]
		self.pid = process._pid
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

	def __init__(self):
		pass