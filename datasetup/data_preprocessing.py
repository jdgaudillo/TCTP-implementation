import pandas as pd 
import numpy as np
import re

from datasetup.utils import *

def clean(filename):
	checkFileType(filename)
	data = openFile(filename)
	data = dropCols(data, features = ['UNNAMED: 0', 'PR', 'GROUP', 'GEOMETRY'])
	validate(data)

	data = addID(data)
	data = dropCols(data, features = ['NAME', 'YEAR', 'TIME'])
	
	print(data.shape)

	time_steps = data['ADV'].values
	regx = re.compile(r'[a-zA-z]$')
	time_steps = [re.sub(regx, '', str(time_step)) for time_step in time_steps]
	data.loc[:, 'ADV'] = time_steps

	TCID = data['TCID'].unique()
	data = data.groupby('TCID', sort=False, group_keys=False).apply(lambda x: x.drop_duplicates('ADV', keep='last'))

	status = data['STAT'].values
	status = [stat.replace(' ', '') for stat in status]
	print(data['STAT'].unique())

	out_file = 'exported/Cleaned_Dataset.csv'
	toCSV(data, out_file)
