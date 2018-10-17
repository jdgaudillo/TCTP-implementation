import warnings
warnings.filterwarnings('ignore')

from datasetup.data_preprocessing import *
from datasetup.data_segmentation import *
from datasetup.data_transformation import *


data_filename = 'imported/Full_Dataset.txt'

data = openFile(filename)

data = cleanData(data)


filter_mode = # ORIGIN or ENDPOINT
filtered_data = filterPAR(data, filter_mode = filter_mode)

normalized_data = normalized(filtered_data)

segmentation_mode = # 1: kmeans, 2: hierarchical clustering, 3: DBSCAN
features = # list of features

if segmentation_mode == 1:
	cluster_dict = kmeans(normalized_data, features = features)
elif segmentation_mode == 2:
	cluster_dict = hierarchicalCLustering(normalized_data, features = features)
else:
	cluster_dict = DBSCAN(normalized_data, features = features)


transformation_mode = # 1: component method, 2: point-time equivalence, 3: z-order 

cluster_number = # Label of cluster
input_data = clusterDataframe(cluster_dict, cluster_number = cluster_number)

if transformation_mode == 1: 
	lat_data, long_data = componentMethod(input_data)
elif transformation_mode == 2:
	T2_data = PTEquivalence(input_data)
else:
	T3_data = zOrder(input_data) 

print('hello')