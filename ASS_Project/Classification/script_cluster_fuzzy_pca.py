# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 19:33:22 2019

@author: u21501882
"""


import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler

from fcmeans import FCM


#data = np.loadtxt('Vecteurs.csv', delimiter=';', skiprows=1)
data = np.loadtxt('Vecteurs_3_300.csv', delimiter=',', skiprows=1)

print(data.shape)
X = data
X = StandardScaler().fit_transform(X)

#
#
#X, y_true = make_blobs(n_samples=300, centers=4,
#                       cluster_std=0.60, random_state=0)

print(type(X))
print(X.shape)
print("------------")

#test
# Import PCA Algorithm
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
# Get the eigenvalues
#pca.explained_variance_ratio
#test

# fit the fuzzy-c-means
fcm = FCM(n_clusters=3)
fcm.fit(te)

# outputs
centers = fcm.centers
y_kmeans = fcm.u.argmax(axis=1)



#nmbre cluster

t = []
for k in y_kmeans:
        if not k in t:
            t.append(k)
        else:
            r="mince"
print("nbr clust : "+str(len(t)))
#fin nmbre cluster

plt.scatter(te[:, 0], te[:, 1], c=y_kmeans, s=50, cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
