# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 04:16:49 2019

@author: u21501882
"""

from sklearn.cluster import DBSCAN

from keras.layers import Input, Dense
from keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

data = np.loadtxt('Vecteurs_3_300.csv', delimiter=',',skiprows=1)
#
#print(data.shape)
X=data
train = StandardScaler().fit_transform(X)

encoding_dim = 2
input_layer = Input(shape=(train.shape[1],))
encoded = Dense(encoding_dim, activation='relu')(input_layer)
decoded = Dense(train.shape[1], activation='sigmoid')(encoded)

# let's create and compile the autoencoder
autoencoder = Model(input_layer, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

from sklearn.model_selection import train_test_split
#X1, X2, Y1, Y2 = train_test_split(train, train, test_size=0.2, random_state=42)

# these parameters seems to work for the Mercedes dataset
autoencoder.fit(train, train,
                epochs=300,
                batch_size=200,
                shuffle=False,
                verbose = 2,
                validation_data=(X2, Y2))

# now let's evaluate the coding of the initial features
encoder = Model(input_layer, encoded)
preds = encoder.predict(train)



# Compute DBSCAN
db = DBSCAN(eps=0.5, min_samples=10,metric="euclidean",algorithm="auto").fit(preds)
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

