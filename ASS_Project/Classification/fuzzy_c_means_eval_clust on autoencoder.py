# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 04:24:13 2019

@author: u21501882
"""

from __future__ import division, print_function
import skfuzzy as fuzz
from keras.layers import Input, Dense
from keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# 1 - Data importing - data process

colors = ['b', 'orange', 'g', 'r', 'c', 'm', 'y', 'k', 'Brown', 'ForestGreen']

data = np.loadtxt('Vecteurs_3_300.csv', delimiter=',',skiprows=1)
#
#print(data.shape)
X=data
train = StandardScaler().fit_transform(X)

# 2 - Autoencoder - dimension reduction
encoding_dim = 2
input_layer = Input(shape=(train.shape[1],))
encoded = Dense(encoding_dim, activation='relu')(input_layer)
decoded = Dense(train.shape[1], activation='sigmoid')(encoded)

# let's create and compile the autoencoder
autoencoder = Model(input_layer, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

from sklearn.model_selection import train_test_split
X1, X2, Y1, Y2 = train_test_split(train, train, test_size=0.2, random_state=42)

# these parameters seems to work for the Mercedes dataset
autoencoder.fit(X1, Y1,
                epochs=300,
                batch_size=200,
                shuffle=False,
                verbose = 2,
                validation_data=(X2, Y2))

# now let's evaluate the coding of the initial features
encoder = Model(input_layer, encoded)
preds = encoder.predict(train)

# 3 - Fuzzy C-mean - clustering with evaluation (Fuzzy partition coefficient)
xpts = preds[:,0]
ypts = preds[:,1]
#for i, ((xmu, ymu), (xsigma, ysigma)) in enumerate(zip(centers, sigmas)):
#xpts = np.hstack((xpts))
#ypts = np.hstack((ypts))
# Set up the loop and plot
fig1, axes1 = plt.subplots(3, 3, figsize=(8, 8))
alldata = np.vstack((xpts, ypts))
fpcs = []

for ncenters, ax in enumerate(axes1.reshape(-1), 2):
    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
        alldata, ncenters, 2, error=0.005, maxiter=1000, init=None)

    # Store fpc values for later
    fpcs.append(fpc)

    # Plot assigned clusters, for each data point in training set
    cluster_membership = np.argmax(u, axis=0)
    for j in range(ncenters):
        ax.plot(xpts[cluster_membership == j],
                ypts[cluster_membership == j], '.', color=colors[j])

    # Mark the center of each fuzzy cluster
    for pt in cntr:
        ax.plot(pt[0], pt[1], 'rs')

    ax.set_title('Centers = {0}; FPC = {1:.2f}'.format(ncenters, fpc))
    ax.axis('off')

fig1.tight_layout()


fig2, ax2 = plt.subplots()
ax2.plot(np.r_[2:11], fpcs)
ax2.set_xlabel("Number of centers")
ax2.set_ylabel("Fuzzy partition coefficient")