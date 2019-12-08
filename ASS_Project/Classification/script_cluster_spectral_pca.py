# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 19:33:22 2019

@author: u21501882
"""


import matplotlib.pyplot as plt

from sklearn.datasets.samples_generator import make_blobs

from numpy import genfromtxt,loadtxt
import numpy as np
from sklearn.preprocessing import StandardScaler


#data = np.loadtxt('Vecteurs.csv', delimiter=';', skiprows=1)
data = np.loadtxt('Vecteurs_3_300.csv', delimiter=',',skiprows=1)

print(data.shape)
X=data
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


from sklearn.cluster import SpectralClustering 


# Building the clustering model 
spectral_model_rbf = SpectralClustering(n_clusters = 3, affinity ='rbf') 
  
# Training the model and Storing the predicted cluster labels 
y_kmeans = spectral_model_rbf.fit_predict(te) 


#nmbre cluster

t=[]
for k in y_kmeans:
        if not k in t:
            t.append(k)
        else:
            r="mince"
print("nbr clust : "+str(len(t)))
#fin nmbre cluster

plt.scatter(te[:, 0], te[:, 1], c=y_kmeans, s=50, cmap='viridis')

#plt.clf()


#
#cost =[] 
#for i in range(1, 60): 
#    KM = KMeans(n_clusters = i, max_iter = 500) 
#    KM.fit(te) 
#      
#    # calculates squared error 
#    # for the clustered points 
#    cost.append(KM.inertia_)      
#  
## plot the cost against K values 
#plt.plot(range(1, 60), cost, color ='g', linewidth ='3') 
#plt.xlabel("Value of K") 
#plt.ylabel("Sqaured Error (Cost)") 
#plt.show() # clear the plot 
  
# the point of the elbow is the  
# most optimal value for choosing k 