import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.cluster import KMeans

#____________________________FUNCTIONS__________________________

def values_kmeans(centers = 0):
    global c1, c2
    if centers:
        c1, c2 = centers[0], centers[1]
        return True
    else:
        return False

def k_means(i, x, y):
    
    global dataset

    #classifier
    kmeans = KMeans(n_clusters = 2, 
            init='random',
            n_init=1,
            max_iter=2)
    
    if values_kmeans():
        
        #using the centers of the previous execution 
        kmeans.cluster_centers_[:,0] = c1
        kmeans.cluster_centers_[:,1] = c2

    predict_y = kmeans.fit_predict(dataset)

    values_kmeans([kmeans.cluster_centers_[:,0],
                  kmeans.cluster_centers_[:,1]])

    # i forgot how to manipulate an numpy array, so i convert then in lists 
    copy_x = list(dataset[:,0]) + [kmeans.cluster_centers_[:,0][0]] + [kmeans.cluster_centers_[:,0][1]]
    copy_y = list(dataset[:,1]) + [kmeans.cluster_centers_[:,1][0]] + [kmeans.cluster_centers_[:,1][1]]
        
    colors = list(predict_y) + [2, 3]

    #plotting the graphics
    ax.clear()
    ax.scatter(copy_x, copy_y, s = 70, c = colors)

#__________________________GLOBAL VARIABLES___________________________

c1 = [0, 0]
c2 = [0, 0]

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

#_________________DINAMIC GRAPHIC________________________

figure = plt.figure()
ax = figure.add_subplot(1, 1, 1)
ani = animation.FuncAnimation(figure, k_means, fargs=([0], [0]), interval=100)
plt.show()