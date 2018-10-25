import pandas as pd 
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
from matplotlib import pyplot as plt

# from utils import *


def kmeans(data, centroids):  # input pandas ORIGIN DataFrame, output additional row in original data set
    df = data[['TCID', 'LATITUDE', 'LONGITUDE']].set_index('TCID')
    k_means = KMeans(n_clusters = centroids)
    k_means.fit(df)

    # centroids = k_means.cluster_centers_
    labels = k_means.labels_

    # print(centroids)
    # print(labels)

    data['K-Means Labels'] = labels
    return data


def hierarchicalclustering(data, features):
    return


def DBSCAN(data, features):
    return


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
    outfile = 'exported/Silhouette_Analysis_Plot_1/0.jpg'
    plt.savefig('exported/plots/Silhouette_Analysis_Plot_filter.png')
    plt.close()
    return


def elbow_plot_analysis(data):
    data = data[['LATITUDE', 'LONGITUDE']]
    distortions = []
    k = range(1, 101)
    for i in k:
        k_means = KMeans(n_clusters = i).fit(data)
        k_means.fit(data)
        distortions.append(sum(np.min(cdist(data, k_means.cluster_centers_, 'euclidean'), axis = 1)) / data.shape[0])

    plt.plot(k, distortions, 'rx-')
    plt.xlabel('Number of Centroids')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal Number of Centroids')
    plt.show()

    return
