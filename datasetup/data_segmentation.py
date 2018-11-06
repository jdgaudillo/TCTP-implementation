import warnings
import matplotlib as mpl
mpl.use('Tkagg')
from sklearn.cluster import MeanShift
from sklearn.cluster import DBSCAN
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import matplotlib.cm as cm

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
    """ Performs Hierarchical Clustering clustering using MeanShift

        Parameters
        -----------
        data: dataframe
            The dataframe which contains the data

        Returns
        -----------
        data: dataframe
            Dataframe which contains Hierarchical Clustering  Labels (cluster label of each tropical cyclone)
        """
    copy = data[['LATITUDE', 'LONGITUDE', 'TCID']].set_index('TCID')
    ms = MeanShift()
    ms.fit(copy)
    lbs = ms.labels_
    data['Hierarchical Clustering Label'] = lbs
    return data


def DBSCANClustering(data):
    """ Performs DBSCAN clustering

        Parameters
        -----------
        data: dataframe
            The dataframe which contains the data

        Returns
        -----------
        data: dataframe
            Dataframe which contains DBSCAN Labels (cluster label of each tropical cyclone)
        """
    copy = data[['LATITUDE', 'LONGITUDE', 'TCID']].set_index('TCID')
    db = DBSCAN(eps = 0.3).fit(copy)
    labels = db.labels_
    data['DBSCAN Labels'] = labels
    return data


def silhouetteAnalysis(data, name, add):
    """ Performs silhouette analysis

    Parameters
    -----------
    data: dataframe
        The dataframe which contains the data

    name: String
        Name of the output plot

    add: String
        Name of additional filename

    Returns
    -----------
    plot: png
        Silhouette Analysis plot
    """

    data = data[['LATITUDE', 'LONGITUDE']]
    data = data.values
    sil_list = []
    k = range(2, 10)

    ncluster = []
    silhouetteavg = []

    for n_cluster in k:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches(18, 7)

        ax1.set_xlim([-0.1, 1])
        ax1.set_ylim([0, len(data) + (n_cluster + 1) * 10])

        k_means = KMeans(n_clusters = n_cluster, random_state=42)

        cluster_labels = k_means.fit_predict(data) 
        sil_list.append(metrics.silhouette_score(data, cluster_labels, metric = 'euclidean'))
        silhouette_avg = metrics.silhouette_score(data, cluster_labels)

        ncluster.append(n_cluster)
        silhouetteavg.append(silhouette_avg)

        sample_silhouette_values = metrics.silhouette_samples(data, cluster_labels)
        y_lower = 10

        for i in range(n_cluster):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values = \
                sample_silhouette_values[cluster_labels == i]

            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = cm.nipy_spectral(float(i) / n_cluster)
            ax1.fill_betweenx(np.arange(y_lower, y_upper),
                              0, ith_cluster_silhouette_values,
                              facecolor=color, edgecolor=color, alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster label")

        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

        # 2nd Plot showing the actual clusters formed
        colors = cm.nipy_spectral(cluster_labels.astype(float) / n_cluster)
        ax2.scatter(data[:, 0], data[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                    c=colors, edgecolor='k')

        # Labeling the clusters
        centers = k_means.cluster_centers_
        # Draw white circles at cluster centers
        ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
                    c="white", alpha=1, s=200, edgecolor='k')

        for i, c in enumerate(centers):
            ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
                        s=50, edgecolor='k')

        ax2.set_title("The visualization of the clustered data.")
        ax2.set_xlabel("Feature space for the 1st feature")
        ax2.set_ylabel("Feature space for the 2nd feature")

        plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                      "with n_clusters = %d" % n_cluster),
                     fontsize=14, fontweight='bold')

        outfile = 'exported/silhouette-plots/silhouette_analysis_distribution_' + str(n_cluster) + '_' + str(add)+'.png'
        plt.savefig(outfile)
        plt.close()

    plt.figure()
    plt.plot(k, sil_list, 'bx-')
    plt.xlabel('Number of Centroids')
    plt.ylabel('Silhouette Score')
    plt.savefig('exported/silhouette-plots/' + str(name))
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
    return
