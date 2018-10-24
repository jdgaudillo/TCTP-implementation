import pandas as pd 
import numpy as np
import re

from shapely import geometry
import time

from datasetup.utils import *

def clean(filename):
	checkFileType(filename)
	data = openFile(filename)
	#data = dropCols(data, features = ['UNNAMED: 0', 'PR', 'GROUP', 'GEOMETRY'])
	validate(data)

	#data = addID(data)
	#data = dropCols(data, features = ['NAME', 'YEAR'])
	
	print(data.shape)

	time_steps = data['ADV'].values
	regx = re.compile(r'[a-zA-z]$')
	time_steps = [re.sub(regx, '', str(time_step)) for time_step in time_steps]
	data.loc[:, 'ADV'] = time_steps

	TCID = data['TCID'].unique()
	data = data.groupby('TCID', sort=False, group_keys=False).apply(lambda x: x.drop_duplicates('ADV', keep='last'))

	status = data['STAT'].values
	status = [stat.replace(' ', '') for stat in status]

	print('Successfully cleaned file')
	
	return data

def getPoints(data, mode):
	start_time = time.time()
	TCID = data.TCID.unique.values
	if mode == 'ORIGIN':
		data = data.drop(data[data['ADV'] != '1'].index)
	elif mode == 'ENDPOINT':
		TCID_len = len(TCID) 
		for TC in TCID:
			duration = len(data.loc[data['TCID'] == TC])
			endpoint_index = duration - 1
			endpoint = data.iloc[[endpoint_index]]
			data = data.drop(data[data['TCID'] == TC].index)
			data = pd.concat([data, endpoint])

	print('Run Time: %s seconds' % (time.time() - start_time))
	print('Successfully extracted', mode, 'points')

	return data


def filterPAR(data):
	TCID_par = []
	par_poly = geometry.Polygon([(120, 25), (135, 25), (135, 5), (115, 5), (115, 15), (120, 21), (120, 25)])
	start_time = time.time()

	for TCID, val in data.groupby('TCID', sort=False):
		trajectory = geometry.MultiPoint(val[['LONGITUDE', 'LATITUDE']].values)
						
		if trajectory.intersects(par_poly):
			TCID_par.append(TCID)
					
	print("Run Time: %s seconds" % (time.time() - start_time))

	data = data.loc[data['TCID'].isin(TCID_par)].reset_index(drop=True)

	print('Successfully filtered data that passed through PAR')

	return data

def normalize(filename):
	checkFileType(filename)
	data = openFile(filename)

	TCIDs = data['TCID'].values
	origin_array = data.loc[data['ADV'] == '1', ['LATITUDE', 'LONGITUDE']].values
	
	
	origin_dict = dict(zip(TCIDs, origin_array))

	for TCID, origin in origin_dict.items():
		latitude = data.loc[data['TCID'] == TCID, 'LATITUDE'].values
		longitude = data.loc[data['TCID'] == TCID, 'LONGITUDE'].values
		
		norm_lat = [np.round(lat-origin[0], 2) for lat in latitude]
		norm_long = [np.round(lon - origin[1], 2) for lon in longitude]

		data.loc[data['TCID'] == TCID, 'NORMALIZED_LATITUDE'] = norm_lat
		data.loc[data['TCID'] == TCID, 'NORMALIZED_LONGITUDE'] = norm_long
	
	out_file = 'exported/' + 'Normalized_Dataset.csv'
	toCSV(data, out_file)
