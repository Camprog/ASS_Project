# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 01:56:09 2019

@author: u21501882
"""

import numpy as np 
import pandas as pd 
from sklearn.cluster import MeanShift 
from sklearn.datasets.samples_generator import make_blobs 
from matplotlib import pyplot as plt 
from sklearn.preprocessing import StandardScaler

from mpl_toolkits.mplot3d import Axes3D 
   
# We will be using the make_blobs method 
# in order to generate our own data. 
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

   
# After training the model, We store the 
# coordinates for the cluster centers 
ms = MeanShift() 
ms.fit(te) 
centers = ms.cluster_centers_ 
y_kmeans=ms.predict(te)

plt.scatter(te[:, 0], te[:, 1], c=y_kmeans, s=50, cmap='viridis')

plt.scatter(centers[:, 0], centers[:, 1], c='black', s=100, alpha=1);

# Finally We plot the data points 
# and centroids in a 3D graph. 
#fig = plt.figure() 
#  
#ax = fig.add_subplot(111, projection ='3d') 
#  
#ax.scatter(X[:, 0], X[:, 1], X[:, 2], marker ='o') 
#  
#ax.scatter(cluster_centers[:, 0], cluster_centers[:, 1], 
#           cluster_centers[:, 2], marker ='x', color ='red', 
#           s = 300, linewidth = 5, zorder = 10) 
#  
#plt.show() 