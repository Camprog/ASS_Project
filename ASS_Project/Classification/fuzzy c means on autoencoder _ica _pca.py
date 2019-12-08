# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 03:45:34 2019

@author: u21501882
"""

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





from fcmeans import FCM

# fit the fuzzy-c-means
fcm1 = FCM(n_clusters=3)
fcm1.fit(preds)

# outputs
centers = fcm1.centers
y_kmeans1 = fcm1.u.argmax(axis=1)




#plt.scatter(preds[:, 0], preds[:, 1], c=y_kmeans1, s=50, cmap='viridis')
#
#plt.scatter(centers[:, 0], centers[:, 1], c='black', s=100, alpha=1);
##plt.clf()
plt.figure(figsize = (17,5))
plt.subplot(131)
plt.scatter(preds[:, 0], preds[:, 1], c=y_kmeans1, s=50, cmap='viridis')

plt.scatter(centers[:, 0], centers[:, 1], c='black', s=100, alpha=1);
plt.title('AE Scatter Plot')

#pca ica
from sklearn.decomposition import PCA, FastICA # Principal Component Analysis module
ica = FastICA(n_components=2)
ica_2d = ica.fit_transform(train)



# ica




# fit the fuzzy-c-means
fcm2 = FCM(n_clusters=3)
fcm2.fit(ica_2d)

# outputs
centers = fcm2.centers
y_kmeans2 = fcm2.u.argmax(axis=1)

plt.subplot(132)
plt.scatter(ica_2d[:, 0], ica_2d[:, 1], c=y_kmeans2, s=50, cmap='viridis')

plt.scatter(centers[:, 0], centers[:, 1], c='black', s=100, alpha=1);
plt.title('ICA Scatter Plot')

#pca


pca = PCA(n_components=2)
pca_2d = pca.fit_transform(train)


# fit the fuzzy-c-means
fcm2 = FCM(n_clusters=3)
fcm2.fit(pca_2d)

# outputs
centers = fcm2.centers
y_kmeans3 = fcm2.u.argmax(axis=1)

plt.subplot(133)
plt.scatter(pca_2d[:, 0], pca_2d[:, 1], c=y_kmeans3, s=50, cmap='viridis')

plt.scatter(centers[:, 0], centers[:, 1], c='black', s=100, alpha=1);
plt.title('PCA Scatter Plot')

plt.show()