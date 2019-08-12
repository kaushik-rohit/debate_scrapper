import csv
import os
import json
import re

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def convert_to_csv():
	filenames = os.listdir(data_path)
	filenames = [f for f in filenames if f.endswith('.json') ]
	filenames.sort()
	
	with open('output.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(['date', 'speaker', 'speech'])
		for names in filenames:
			filepath = os.path.join(data_path, names)
			with open(filepath) as f:
				data = json.load(f)
				if(len(data) == 1):
					continue
				for d in data:
					speech = d['speech'].strip()
					speech = re.sub(r'\[[0-9]+\]', '', speech)
					speech = re.sub(r'\s+', ' ', speech)
					writer.writerow([names.replace('.json', ''), d['speaker'][:-1], speech])
		

		
		
if __name__ == '__main__':
	convert_to_csv()
