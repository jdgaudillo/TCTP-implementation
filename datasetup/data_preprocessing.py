import pandas as pd 
import numpy as np
import re

from shapely import geometry
import time

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

def getPoints(data, TCID_par, mode):
	if mode == 'ORIGIN':
		data = data.drop(data[data['ADV'] != '1'].index)
	elif mode == 'ENDPOINT':
		TCID_len = len(TCID_par) 
		for TCID in TCID_par:
			duration = len(data.loc[data['TCID'] == TCID])
			endpoint_index = duration - 1
			endpoint = data.iloc[[endpoint_index]]
			data = data.drop(data[data['TCID'] == TCID].index)
			data = pd.concat([data, endpoint])
	return data


def filterPAR(filename):
	checkFileType(filename)
	data = openFile(filename)

	TCID_par = []
	par_poly = geometry.Polygon([(120, 25), (135, 25), (135, 5), (115, 5), (115, 15), (120, 21), (120, 25)])
	start_time = time.time()

	for TCID, val in data.groupby('TCID', sort=False):
		trajectory = geometry.MultiPoint(val[['LONGITUDE', 'LATITUDE']].values)
						
		if trajectory.intersects(par_poly):
			TCID_par.append(TCID)
					
	print("Run Time: %s seconds" % (time.time() - start_time))

	data = data.loc[data['TCID'].isin(TCID_par)].reset_index(drop=True)

	mode = 'ENDPOINT'
	filtered_data = getPoints(data, TCID_par, mode)
	
	outfile = 'exported/' + mode + '_Data.csv'
	toCSV(filtered_data, outfile)
