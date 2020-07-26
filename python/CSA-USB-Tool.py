import csv
from pprint import pprint
import requests


d = {}
def load_csv():
	with open('FRCSoftware2020.csv') as f:
		headers = [header.strip() for header in next(f).split(",")]

		for line in f:
			values = [value.strip() for value in line.split(",")]
			d[values[0]] = dict(zip(headers, values[0:]))

def fetch_file():
	
load_csv()
for l in d:
	z = d[l]
	print(f'File: {z["FriendlyName"]}')
	print(f'\tDownload url: {z["URL"]}')
	print(f'\tto local Filename: {z["FileName"]}')

	myfile = requests.get(z["URL"], stream = True)
	
	with open(z["FileName"], "wb") as Pypdf:
		total_length = int(myfile.headers.get('content-length'))/1024
		print(f'\tFile size {total_length}')
		
		break
	# next make save-file a routine

		for chunk in myfile.iter_content(chunk_size = 1024*1024):

			if chunk:

				Pypdf.write(chunk)

	#open(z["FileName"], 'wb').write(myfile.content)

	break


#pprint(d)

exit()

