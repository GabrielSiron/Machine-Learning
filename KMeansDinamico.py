from matplotlib import pyplot as plt
from random import uniform

UNITVALUES = 99

CENTERS = 3

def calcEuclidianDistance(x, ref):
    return (x[0]-ref[0])**2 + (x[1]-ref[1])**2

def generateValues():
    return [[uniform(0, 100), uniform(0, 100), 0] for x in range(UNITVALUES)]
    

def generateCenters():
    return [[uniform(0, 100), uniform(0, 100), x] for x in range(CENTERS)]

values = generateValues()

centers = generateCenters()

while True:
    for i in range(UNITVALUES):
        distances = []
        for j in range(CENTERS):
            distances.append(calcEuclidianDistance(values[i], centers[j]))
        values[i][2] = distances.index(min(distances))

    for i in range(UNITVALUES):
        plt.plot(values[i][0], values[i][1], 'o', color=(values[i][2]/CENTERS, values[i][2]/CENTERS, values[i][2]/CENTERS))
    for j in range(CENTERS):
        plt.plot(centers[j][0], centers[j][1], 'o', color=(0.5, 0.2, 0.7))

    plt.draw()
    plt.pause(0.01) 
    plt.clf()
 
    sumValuesX = [0]*CENTERS
    sumValuesY = [0]*CENTERS
    qtdValues = [0]*CENTERS

    for i in range(UNITVALUES):
        qtdValues[values[i][2]] += 1
        sumValuesX[values[i][2]] += values[i][0]
        sumValuesY[values[i][2]] += values[i][1]

    for j in range(CENTERS):
        centers[j][0] = sumValuesX[j]/qtdValues[j]
        centers[j][1] = sumValuesY[j]/qtdValues[j] 
