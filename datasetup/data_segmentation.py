import warnings
warnings.filterwarnings('ignore')

import matplotlib as mpl 
mpl.use('Tkagg')

import pandas as pd 
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt

import pandas as pd

from datasetup.utils import *


def kmeans(data, centroids):  # input pandas ORIGIN DataFrame, output additional row in original data set
    df = data[['TCID', 'LATITUDE', 'LONGITUDE']].set_index('TCID')
    k_means = KMeans(n_clusters = centroids)
    k_means.fit(df)

    centroids = k_means.cluster_centers_
    labels = k_means.labels_

    print(centroids)
    print(labels)

    data['K-Means Labels'] = labels
    return data


#def hierarchicalClustering(data, features):


#def DBSCAN(data, features):


def silhouetteAnalysis(data):  # input pandas ORIGIN DataFrame, output plot
    data = data[['LATITUDE', 'LONGITUDE']]
    sil_list = []
    k = range(2, 50)
    for i in k:
        k_means = KMeans(n_clusters = i)
        k_means.fit(data)

        labels = k_means.labels_

        sil_list.append(metrics.silhouette_score(data, labels, metric = 'euclidean'))

    # plotting for analysis
    plt.figure()
    plt.plot(k, sil_list, 'bx-')
    plt.xlabel('Number of Centroids')
    plt.ylabel('Silhouette Score')
    outfile = 'exported/Silhouette_Analysis_Plot_1/0.jpg'
    plt.savefig('exported/plots/Silhouette_Analysis_Plot_filter.png')
    plt.close()