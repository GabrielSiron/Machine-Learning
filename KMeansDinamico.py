import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.cluster import KMeans

dataset = np.array([[178, 77], 
                    [154, 64],
                    [160, 60],
                    [185, 80],
                    [177, 76],
                    [175, 84],
                    [156, 55],
                    [160, 65],
                    [153, 52],
                    [179, 78],
                    [145, 49],
                    [156, 53],
                    [170, 73],
                    [152, 56],
                    [149, 50],
                    [172, 80],
                    [187, 85],
                    [164, 52],
                    [150, 50],
                    [176, 79]])

kmeans = KMeans(n_clusters = 3, 
        init='random',
        n_init=1,
        max_iter=1)

figure = plt.figure()
ax = figure.add_subplot(1, 1, 1)
qtd = 3
predict_y = []
list_center = [0]*qtd

aux1 = 0
aux2 = 0
aux3 = 0

for j in range(10):
    if j > 0:
        print(kmeans.cluster_centers_)
    predict_y.append(kmeans.fit_predict(dataset))
    print(kmeans.cluster_centers_)

copy_x = list(dataset[:,0])
copy_y = list(dataset[:,1])
for i in range(10):
    ax.clear()
    ax.scatter(copy_x, copy_y, s = 70, c = predict_y[i])
    plt.draw()
    plt.pause(0.001)