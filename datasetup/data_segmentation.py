import pandas as pd 
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
from matplotlib import pyplot as plt
import pandas as pd

from utils import *


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


def hierarchicalClustering(data, features):


def DBSCAN(data, features):


def silhouette_analysis(data):  # input pandas ORIGIN DataFrame, output plot
    data = data[['LATITUDE', 'LONGITUDE']]
    sil_list = []
    k = range(2, 10)
    for i in k:
        k_means = KMeans(n_clusters = i)
        k_means.fit(data)

        labels = k_means.labels_

        sil_list.append(metrics.silhouette_score(data, labels, metric = 'euclidean'))

    # plotting for analysis
    plt.plot(k, sil_list, 'bx-')
    plt.xlabel('Number of Centroids')
    plt.ylabel('Silhouette Score')
    plt.show()
    return