# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 02:42:32 2019

@author: u21501882
"""

from sklearn import cluster
from scipy.spatial import distance
from sklearn.preprocessing import StandardScaler
import numpy as np
from matplotlib import pyplot as plt 


def compute_bic(kmeans, x):
    """
    Computes the BIC metric for a given clusters

    Parameters:
    -----------------------------------------
    kmeans:  List of clustering object from scikit learn

    X     :  multidimension np array of data points

    Returns:
    -----------------------------------------
    BIC value
    """
    # assign centers and labels
    centers = [kmeans.cluster_centers_]
    labels = kmeans.labels_
    #number of clusters
    m = kmeans.n_clusters
    # size of the clusters
    n = np.bincount(labels)
    #size of data set
    N, d = x.shape

    #compute variance for all clusters beforehand
    cl_var = (1.0 / (N - m) / d) * sum([sum(distance.cdist(X[np.where(labels == i)], [centers[0][i]], 'euclidean')**2)
                                        for i in range(m)])

    const_term = 0.5 * m * np.log(N) * (d+1)

    return np.sum([n[i] * np.log(n[i]) - n[i] * np.log(N) - ((n[i] * d) / 2) * np.log(2*np.pi*cl_var) -
                   ((n[i] - 1) * d/2) for i in range(m)]) - const_term


X = np.loadtxt('Vecteurs_3_300.csv', delimiter=',',skiprows=1)
X = StandardScaler().fit_transform(X)


ks = range(1,20)

# run 9 times kmeans and save each result in the KMeans object
KMeans = [cluster.KMeans(n_clusters=i, init="k-means++").fit(X) for i in ks]

# now run for each cluster the BIC computation
BIC = [compute_bic(kmeansi, X) for kmeansi in KMeans]

plt.plot(ks, BIC, 'r-o')
plt.title("data  (cluster vs BIC)")
plt.xlabel("# clusters")
plt.ylabel("# BIC")