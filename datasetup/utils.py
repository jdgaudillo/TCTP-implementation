import pandas as pd
import numpy as np
import sys
import time

def checkFileType(filename):
	""" Checks if input filename has correct filetype (e.g. csv, txt, xlsx)

	Parameters
	-----------
	filename: str
		The filename of the dataset

	Returns
	-----------
		[Stops the execution of the code if input file type is incorrect]
	"""

	filetypes = ('.csv', '.txt', '.xlsx')
	success = 0

	if filename.endswith(filetypes):
		success = 1

	if success == 0:
		sys.exit('ERROR: Improper file format!')

	print('Correct file format!\n')



def openFile(filename):
	""" Opens input file and store content to dataframe

	Parameters
	-----------
	filename: str
		The filename of the dataset

	Returns
	-----------
	data: dataframe
		A dataframe containing the contents of the input file

	"""

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
	""" Validates data content

	Parameters
	-----------
	data: dataframe
		The dataframe which contains the content of the input file

	Returns
	-----------
	"""

	dtype_float = ['float', 'ADV', 'LATITUDE', 'LONGITUDE', 'WIND']


	float_dict = {'LATITUDE': 'float64', 'LONGITUDE': 'float64', 
			'WIND': 'float64'}

	

def addID(data):
	""" Adds ID field to the dataframe

	Parameters
	-----------
	data: dataframe
		The dataframe which contains the content of the input file

	Returns
	-----------
	data: dataframe
		Dataframe with TCID field

	"""

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
	""" Drops columns indicated by the features

	Parameters
	-----------
	data: dataframe
		The dataframe which contains the content of the input file
	features: array
		Array of features to drop

	Returns
	-----------
	data: dataframe
	"""

	data.rename(columns = lambda x: x.upper(), inplace=True)
	data = data.drop(features, axis=1)

	return data



def toCSV(data, out_file):
	""" Saves dataframe to csv file

	Parameters
	-----------
	data: dataframe
		The dataframe which contains the content of the input file
	outfile: str
		Output filename

	Returns
	-----------
	"""
	data.to_csv(out_file, index = False)

