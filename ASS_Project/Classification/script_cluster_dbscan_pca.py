# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 23:49:50 2019

@author: u21501882
"""

from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

#X = np.array([[1, 2], [2, 2], [2, 3],
#              [8, 7], [8, 8], [25, 80]])

#data = np.loadtxt('Vecteurs.csv', delimiter=';', skiprows=1)
data = np.loadtxt('Vecteurs_3_300.csv', delimiter=',',skiprows=1)
#
#print(data.shape)
X=data
X = StandardScaler().fit_transform(X)

from sklearn.decomposition import PCA

# Initialize the algorithm and set the number of PC's
pca = PCA(n_components=2)

# Fit the model to data 
pca.fit(X)
# Get list of PC's
pca.components_
# Transform the model to data 
te=pca.transform(X)
print(te)

#
#clustering = DBSCAN(eps=3,min_samples=2).fit(te)
#
#
#Result=clustering.labels_
#y_kmeans = clustering.fit_predict(te)
# Compute DBSCAN
db = DBSCAN(eps=0.5, min_samples=17,metric="euclidean",algorithm="auto").fit(te)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)
#print(Result)


#nmbre cluster

t=[]
for k in labels:
        if not k in t:
            t.append(k)
        else:
            r="mince"
print(t)
        
#print(clustering )

# #############################################################################
# Plot result

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

#    xy = X[class_member_mask & ~core_samples_mask]
#    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
#             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()