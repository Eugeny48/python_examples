import argparse
import threading
import random
from time import sleep

lock = threading.Lock()

def main():
	parser = argparse.ArgumentParser(
		description="Prints multiplication table",
	)
	parser.add_argument("from1", nargs="?", default=1)
	parser.add_argument("to1", nargs="?", default=10)
	parser.add_argument("from2", nargs="?", default=1)
	parser.add_argument("to2", nargs="?", default=10)

	args = parser.parse_args()

	collection = dict()

	threads = [threading.Thread(target=buildTable, args=(n1, int(args.from2), int(args.to2), collection)) for n1 in range(int(args.from1), int(args.to1) + 1)]
	for thread in threads:
		thread.start()

	while len(collection) < len(threads):
		sleep(0.1)

	for table in collection.values():
		print(table + "\n")


def buildTable(n1 : int, n2from : int, n2to : int, collection : dict=None):
	sleep(random.random() * 5)
	table = "\n".join(("%i * %i = %i" % (n1, n2, n1 * n2) for n2 in range(n2from, n2to + 1)))
	if collection != None:
		with lock:
			collection[n1] = table
	else:
		return table

main()
