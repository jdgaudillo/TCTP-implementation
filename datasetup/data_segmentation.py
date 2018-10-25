import warnings
import matplotlib as mpl
from sklearn.cluster import MeanShift
from sklearn.cluster import DBSCAN
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
mpl.use('Tkagg')
# from utils import *


def kmeans(data, centroids): 
    """ Performs kMeans clustering

    Parameters
    -----------
    data: dataframe
        The dataframe which contains the data
    centroids: int
        Number of centroids 

    Returns
    -----------
    data: dataframe
        Dataframe which contains K-Means Labels (cluster label of each tropical cyclone)
    """

    df = data[['TCID', 'LATITUDE', 'LONGITUDE']].set_index('TCID')
    k_means = KMeans(n_clusters = centroids)
    k_means.fit(df)

    labels = k_means.labels_

    data['K-Means Labels'] = labels

    # print(centroids)
    # print(labels)

    data['K-Means Label'] = labels
    return data


def hierarchicalClustering(data):
    copy = data[['LATITUDE', 'LONGITUDE', 'TCID']].set_index('TCID')
    ms = MeanShift()
    ms.fit(copy)
    lbs = ms.labels_
    data['Hierarchical Clustering Label'] = lbs
    return data


def DBSCANClustering(data):
    copy = data[['LATITUDE', 'LONGITUDE', 'TCID']].set_index('TCID')
    db = DBSCAN(eps = 0.3).fit(copy)
    labels = db.labels_
    data['DBSCAN Labels'] = labels
    return data


def silhouette_analysis(data):
    """ Performs silhouette analysis

    Parameters
    -----------
    data: dataframe
        The dataframe which contains the data

    Returns
    -----------
    plot: png
        Silhouette Analysis plot
    """

    data = data[['LATITUDE', 'LONGITUDE']]
    sil_list = []
    k = range(2, 50)
    for i in k:
        k_means = KMeans(n_clusters = i)
        k_means.fit(data)

        labels = k_means.labels_

        sil_list.append(metrics.silhouette_score(data, labels, metric = 'euclidean'))

    plt.figure()
    plt.plot(k, sil_list, 'bx-')
    plt.xlabel('Number of Centroids')
    plt.ylabel('Silhouette Score')
    outfile = 'exported/Silhouette_Analysis_Plot_1/0.jpg'
    plt.savefig('exported/plots/Silhouette_Analysis_Plot_filter_ztransformed.png')
    plt.close()
    return


def elbowPlotAnalysis(data):
    """ Performs elbow curve analysis

    Parameters
    -----------
    data: dataframe
        The dataframe which contains the data

    Returns
    -----------
    plot: png
        Elbow curve analysis plot
    """

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
    plt.savefig('exported/plots/Elbow_Plot_Analysis_filter_ztransformed.png')
    plt.close()