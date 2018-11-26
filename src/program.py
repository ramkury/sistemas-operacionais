from queue_module import ready_process_queue
from process_module import process, process_manager
from file_module import FileSystem
from dispatcher import dispatcher
import sys

def main():
	procs_file = sys.argv[1] if len(sys.argv) > 1 else "input_files/processes.txt"
	files_file = sys.argv[2] if len(sys.argv) > 2 else "input_files/files.txt"
	processes = read_processes_file(procs_file)
	manager = process_manager()
	_dispatcher = dispatcher(processes)
	while _dispatcher.has_processes() or manager.has_processes():
		_dispatcher.run(manager)
		manager.run()

	fs = FileSystem(files_file)
	fs.run_operations(processes)
	fs.print_disk_occup_map()
	
	print("Done")


def read_processes_file(file_name):
	with open(file_name, 'r') as file:
		lines = [line for line in file.readlines()]
	procs = [process(info) for info in lines]
	return procs


if __name__ == "__main__":
	main()