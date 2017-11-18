import csv
import sys

# чтение параметров
source_file, target_file = sys.argv[1:3]

with open(source_file) as src, open(target_file) as trg:
	reader = csv.DictReader(h)
	writer = csv.DictWriter(h, ['A', 'B', 'X'])
	writer.writeheader()

	for line in reader:
		line['X'] = line['A'] * line['B']

		writer.write(line)
