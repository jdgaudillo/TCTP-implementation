import warnings
warnings.filterwarnings('ignore')

from datasetup.utils import *
from datasetup.data_preprocessing import filterPAR, getPoints
from datasetup.data_segmentation import *

data_file = 'exported/Cleaned_Dataset.csv'

""" User Input Declaration:

	1. filter_mode = 0 (Don't filter); 1 (Filter TC that passed through PAR)
	2. point_mode = 0 (ORIGIN); 1 (ENDPOINT)
	3. clustering_mode = 0 (kMeans); 1 (Hierarchical Clustering); 2 (DBSCAN) 

"""

#filter_mode = input('Filter dataset? \n 0 NO \n 1 YES\n')
#point_mode = input('What data point to use? \n 0 ORIGIN \n 1 ENDPOINT \n')
#clustering_mode = input('What clustering method to use? \n 0 kMeans \n 1 Hierarchical Clustering \n 2 DBSCAN \n')

checkFileType(data_file)
data = openFile(data_file)

if filter_mode == 1:
    filter_mode(data)
    		

if filter_mode == 1:
	data = filterPAR(data)

if point_mode == 0:
	data = getPoints(data, 'ORIGIN')
elif point_mode == 1:
	data = getPoints(data, 'ENDPOINT')

for i in range(3):
	if i == 0:
		sillhouetteAnalysis(data)
	elif i == 1:
		hierarchicalClustering(data)
	elif i == 3:
		DBSCANClustering(data)

