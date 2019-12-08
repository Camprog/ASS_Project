# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 19:33:22 2019

@author: u21501882
"""


import matplotlib.pyplot as plt

from sklearn.datasets.samples_generator import make_blobs

from numpy import genfromtxt,loadtxt
import numpy as np

#data = np.loadtxt('Vecteurs.csv', delimiter=';', skiprows=1)
data = np.loadtxt('Vecteurs_6000.csv', delimiter=',',skiprows=1)

print(data.shape)
X=data
#
#
#X, y_true = make_blobs(n_samples=300, centers=4,
#                       cluster_std=0.60, random_state=0)

print(type(X))
print(X.shape)
print("------------")

#test
# Import PCA Algorithm
# Import Independent Component Analysis Algorithm
from sklearn.decomposition import FastICA

# Initialize the algorithm and set the number of PC's
ica = FastICA(n_components=2)

# Fit and transform the model to data. It returns a list of independent components 
te=ica.fit_transform(data)
print(te)
# Get the eigenvalues
#pca.explained_variance_ratio
#test


from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=4)
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

plt.scatter(te[:, 0], te[:, 1], c=y_kmeans, s=50, cmap='viridis')

#centers = kmeans.cluster_centers_
#plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);