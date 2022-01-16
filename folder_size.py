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


def get_folder_size(path : str, processes_count : int=None) -> dict:
	total_size = 0
	errors_count = 0
	tm0 = time.time()
	with  multiprocessing.Pool(processes=processes_count or multiprocessing.cpu_count()) as pool:
		active_tasks_cnt = 0

		def add_task(path : str):
			nonlocal active_tasks_cnt, pool
			active_tasks_cnt += 1
			pool.apply_async(process_folder, (path,), callback=process_result, error_callback=process_error)

		def process_result(size_and_folders):
			nonlocal total_size, active_tasks_cnt
			if DEBUG:
				print(threading.current_thread().name, multiprocessing.current_process().name)
			size, folders = size_and_folders
			total_size += size
			for path in folders:
				add_task(path)
			active_tasks_cnt -= 1

		def process_error(err):
			nonlocal active_tasks_cnt, errors_count
			print(err)
			errors_count += 1
			active_tasks_cnt -= 1


		add_task(path)

		while active_tasks_cnt:
			time.sleep(0.05)

	result = {
		"size": total_size,
		"time": time.time() - tm0
	}
	if errors_count:
		result["errors_count"] = errors_count

	return result


def main():
	parser = argparse.ArgumentParser(
		description="Calculate folder size",
	)
	parser.add_argument("path", nargs="?", default=".")
	parser.add_argument("processes", nargs="?", type=int, default=multiprocessing.cpu_count())

	args = parser.parse_args()

	result = get_folder_size(args.path, args.processes)

	print(f"Size of `{args.path}` is {result['size']:,}")
	if "errors_count" in result:
		print(f"Warning: {result['errors_count']:,} errors occurred")
	print(f"Processed in {result['time']:.2f} seconds")


if __name__ == '__main__':
	main()
