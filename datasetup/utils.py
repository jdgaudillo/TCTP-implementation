import pandas as pd
import numpy as np
import sys
import time

def checkFileType(filename):
	filetypes = ('.csv', '.txt', '.xlsx')
	success = 0

	if filename.endswith(filetypes):
		success = 1

	if success == 0:
		sys.exit('ERROR: Improper file format!')

	print('Correct file format!\n')


def openFile(filename):
	start_time = time.time()
	filetype = filename.split('.')[1]
	txt = 'txt'
	csv = 'csv'

	if filetype == txt:
		data = pd.read_csv(filename, sep = '\t', na_values = ['-'])
	elif filetype == csv:
		data = pd.read_csv(filename, sep = ',', na_values = ['-'])
	else:
		data = pd.read_excel(filename)

	print('Run Time: %s seconds' % (time.time() - start_time))
	print('Successfully opened ', filename, '\n')

	return data


def validate(data):
	dtype_float = ['float', 'ADV', 'LATITUDE', 'LONGITUDE', 'WIND']


	float_dict = {'LATITUDE': 'float64', 'LONGITUDE': 'float64', 
			'WIND': 'float64'}

	

def addID(data):
	names = data['NAME'].values
	names = [name.replace(' ', '') for name in names]

	years = data['YEAR'].values
	years = [str(year).split('.')[0] for year in years]
	TCID = list(zip(names, years))

	TCID = ['-'.join(d) for d in TCID]

	data.loc[:, 'TCID'] = TCID
	cols = data.columns
	cols = cols.insert(0, 'TCID')[:-1]

	return data


def dropCols(data, features):
	data.rename(columns = lambda x: x.upper(), inplace=True)
	data = data.drop(features, axis=1)

	return data


def toCSV(data, out_file):
	data.to_csv(out_file, index = False)

