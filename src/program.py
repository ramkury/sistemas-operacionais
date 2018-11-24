from queue_module import ready_process_queue
from process_module import process, process_manager
from file_module import FileSystem

def main():
	print("Program works!")
	processes = read_processes_file("input_files/processes.txt")
	manager = process_manager(processes)
	while manager.run():
		pass
	
	print("Done")

def read_processes_file(file_name):
	with open(file_name, 'r') as file:
		lines = [l.strip() for l in file.readlines()]
	procs = [process(info) for info in lines]
	return procs

if __name__ == "__main__":
	main()