import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

'''
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

'''


clusters = 3
features = 3
dataset = np.random.rand(250, features)*100
if features == 3:
    figure = plt.figure()
    ax = figure.add_subplot(111, projection='3d')
    #ax.scatter(args[0], args[1], args[2], s = 70, c = predict_y + [5, 5, 5])
if features == 2:
    figure = plt.figure()
    ax = figure.add_subplot(1, 1, 1)
    #

predict_y = []
list_center = [0]*clusters

center = np.random.rand(clusters, features)*100
#center = [[100, 57, 80], [150, 60, 100], [170, 80, 100]]

for j in range(3):
    
    dist = [[], [], []]
    predict = []
    
    for i in range(clusters):
        soma = 0
        for k in range(len(dataset)):
            for y in range(features):
                soma += (center[i][y] - dataset[k][y])**2
            dist[i].append(pow(soma, 0.5))
    
    for i in range(len(dist[0])):
        comp = []
        for j in range(clusters):
            comp.append(dist[j][i])
        
        predict.append(comp.index(min(comp))) 
            
    print(len(dist))

    args   = [[], [], []]
    for a in range(features):
        for r in range(len(dataset)):
            args[a].append(dataset[r][a])
        for t in range(len(center)):
            args[a].append(center[t][a])

    if features == 2:
        ax.scatter(args[0], args[1], s = 70, c = predict + [5, 5, 5])
    elif features == 3:
        ax.scatter(args[0], args[1], args[2], s = 70, c = predict + [5, 5, 5])

    plt.draw()
    plt.pause(0.2)
    ax.clear()
    medias = []
    for q in range(clusters):
        medias.append([0]*features)

    for b in range(len(predict_y)):
        for u in range(features):
            medias[u].append(dataset[b][u])
    
    #print(medias)
    center = [[0]*features]*clusters
    #print(center)
    
    a = 0

    for k in range(len(dataset)):
        for j in range(clusters):
            if predict[k] == j:
                for i in range(features):
                    center[predict[k]][i] += dataset[k][i]
                a += 1
                
    print(predict)
    
    '''
    medias[0] = sum(mediasx[0])/(len(mediasx[0]) + 0.001)
    mediasx[1] = sum(mediasx[1])/(len(mediasx[1]) + 0.001)
    mediasx[2] = sum(mediasx[2])/(len(mediasx[2]) + 0.001)
        
    mediasy[0] = sum(mediasy[0])/(len(mediasy[0]) + 0.001)
    mediasy[1] = sum(mediasy[1])/(len(mediasy[1]) + 0.001)
    mediasy[2] = sum(mediasy[2])/(len(mediasy[2]) + 0.001)
    '''