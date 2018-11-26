from queue_module import ready_process_queue, priority_queue
import memory_module as memory
from resource_module import GerenciadorRecursos

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
		self.resource_manager = GerenciadorRecursos()
		self.ready_queue = ready_process_queue()
		self.running = self.ready_queue.get()
		self.blocked_printer = [priority_queue(), priority_queue()]
		self.blocked_scanner = priority_queue()
		self.blocked_modem = priority_queue()
		self.blocked_disk = [priority_queue(), priority_queue()]
		

	def run(self):
		if not self.running:
			self.running = self.ready_queue.get()
			if not self.running:
				return False

		completed = self.running.run()

		if completed:
			# If process is finished, free its resources
			self._free_resources(self.running)
			self.running = None
		
		elif self.running.priority > 0:
			if self.running.priority < 3:
				# If it is not lowest priority, lower the process's priority
				self.running.priority += 1

			self.ready_queue.put(self.running)
			self.running = None

		return True


	def add_process(self, process):
		address = memory.check_mem(process.priority, process.mem_blocks)
		if address is None:
			return
		process.offset = address
		if self._get_resources(process):
			self.ready_queue.put(process)


	def has_processes(self):
		return self.running or any([q.has_processes() for q in [
			self.ready_queue,
			*self.blocked_printer,
			self.blocked_scanner,
			self.blocked_modem,
			*self.blocked_disk
		]])


	def _get_resources(self, process, index = 0):
		if not process:
			return False
		if process.printer > 0 and index <= 0:
			if not self.resource_manager.solicita_impressora(process.printer):
				self.blocked_printer[process.printer - 1].put(process)
				return False
		if process.scanner > 0 and index <= 1:
			if not self.resource_manager.solicita_scanner():
				self.blocked_scanner.put(process)
				return False
		if process.modem > 0 and index <= 2:
			if not self.resource_manager.solicita_modem():
				self.blocked_modem.put(process)
				return False
		if process.disk > 0:
			if not self.resource_manager.solicita_SATA(process.disk):
				self.blocked_disk[process.disk - 1].put(process)
				return False
		return True
		

	def _free_resources(self, process):
		memory.free_mem(process.offset, process.mem_blocks, process.priority)
		if process.printer > 0:
			self.resource_manager.libera_impressora(process.printer)
			blocked = self.blocked_printer[process.printer - 1].get()
			if self._get_resources(blocked, 0):
				self.ready_queue.put(blocked)
		if process.scanner > 0:
			self.resource_manager.libera_scanner()
			blocked = self.blocked_scanner.get()
			if self._get_resources(blocked, 1):
				self.ready_queue.put(blocked)
		if process.modem > 0:
			self.resource_manager.libera_modem()
			blocked = self.blocked_modem.get()
			if self._get_resources(blocked, 2):
				self.ready_queue.put(blocked)
		if process.disk > 0:
			self.resource_manager.libera_SATA(process.disk)
			blocked = self.blocked_disk[process.disk - 1].get()
			if self._get_resources(blocked, 3):
				self.ready_queue.put(blocked)