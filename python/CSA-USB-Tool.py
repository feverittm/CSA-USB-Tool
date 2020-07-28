import numpy as np
import csv
from pprint import pprint
import requests
import os
from os import path
import sys
import hashlib


d = {}


def headers(f):
	m_headers = [header.strip() for header in next(f).split(",")]
	m_headers[0] = m_headers[0][1:]
	return(m_headers)

def bighash(filename):
	with open(filename, "rb") as f:
		file_hash = hashlib.md5()
		while chunk := f.read(8192):
			file_hash.update(chunk)
	#print(file_hash.hexdigest())
	return(file_hash.hexdigest())


def load_csv(file):
	with open(file) as f:
		n_headers = headers(f)
		for line in f:
			values = [value.strip() for value in line.split(",")]
			d[values[0]] = dict(zip(n_headers, values[0:]))
	pprint(d)

def main():
	load_csv('../FRCSoftware2020.csv')
	for l in d:
		z = d[l]
		print(f'File: {z["FriendlyName"]}')
		print(f'\tDownload url: {z["URL"]}')
		print(f'\tto local Filename: {z["FileName"]}')
		file_name = z["FileName"]

		if (path.exists(file_name)):
			print(f'\tFile Exists')
			digest = bighash(file_name)
			if digest != z["MD5"]:
				print(f'Hex MD5 mismatch!')
				exit()
		else:
			with open(file_name, "wb") as f:
				myfile = requests.get(z["URL"], stream=True)
				total_length = int(myfile.headers.get('content-length'))
				print(f'\tFile size {total_length}')

				if total_length is None:  # no content length header
					f.write(myfile.content)
				else:
					dl = 0
					total_length = int(total_length)
					for data in myfile.iter_content(chunk_size=4096):
						dl += len(data)
						f.write(data)
						done = int(50 * dl / total_length)
						sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
						sys.stdout.flush()

if __name__== "__main__":
   main()
