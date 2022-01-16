import os
import argparse
import multiprocessing
import time

DEBUG = False

if DEBUG:
	import threading


def process_folder(path : str):
	if DEBUG:
		print("Process `{}`, tread `{}`, process `{}`".format(path, threading.current_thread().name, multiprocessing.current_process().name))
	files_size = 0
	folders = []
	for name in os.listdir(path):
		item_path = os.path.join(path, name)
		if os.path.islink(item_path):
			pass
		elif os.path.isdir(item_path):
			folders.append(item_path)
		else:
			files_size += os.path.getsize(item_path)

	return files_size, folders


def main():
	parser = argparse.ArgumentParser(
		description="Calculate folder size",
	)
	parser.add_argument("path", nargs="?", default=".")
	parser.add_argument("processes", nargs="?", default=multiprocessing.cpu_count())

	args = parser.parse_args()

	total_size = 0
	errors_count = 0
	tm0 = time.time()
	with  multiprocessing.Pool(processes=args.processes) as pool:
		active_tasks_cnt = 0

		#lock1 = multiprocessing.Lock()

		def add_task(path : str):
			nonlocal active_tasks_cnt, pool
			active_tasks_cnt += 1
			# callbacks are processing in the Main process, so there is no need for Locks in there
			pool.apply_async(process_folder, (path,), callback=process_result, error_callback=process_error)

		def process_result(size_and_folders):
			nonlocal total_size, active_tasks_cnt #, lock1
			#lock1.acquire()
			if DEBUG:
				print(threading.current_thread().name, multiprocessing.current_process().name)
			size, folders = size_and_folders
			total_size += size
			for path in folders:
				add_task(path)
			active_tasks_cnt -= 1
			#lock1.release()

		def process_error(err):
			nonlocal active_tasks_cnt, errors_count
			print(err)
			errors_count += 1
			active_tasks_cnt -= 1


		add_task(args.path)

		while active_tasks_cnt:
			time.sleep(0.05)

	print(f"Size of `{args.path}` is {total_size:,}")
	if errors_count:
		print(f"Warning: {errors_count:,} errors occurred")
	print(f"Processed in {time.time() - tm0:.2f} seconds")


if __name__ == '__main__':
	main()
