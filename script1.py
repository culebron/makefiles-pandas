
import csv

with open('houses.csv') as src, open('houses-processed.csv') as trg:
	# открыть файл чтения
	reader = csv.DictReader(h)

	# открыть запись и перечислить все поля
	writer = csv.DictWriter(h, ['A', 'B', 'X'])

	# и не забыть записать заголовок
	writer.writeheader()

	# проход строк
	for line in reader:
		line['X'] = line['A'] * line['B']

		writer.write(line)
