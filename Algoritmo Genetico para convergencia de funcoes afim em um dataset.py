from random import uniform
from matplotlib import pyplot as plt

NUMBER_INDIVIDUALS = 15

class Individual:
    def __init__(self, first_generation=False):
        if first_generation:
            self.a = uniform(-10, 10)
            self.b = uniform(-10, 10)
        else:
            for i in range(NUMBER_INDIVIDUALS):
                if i != index:
                    generation[i].a = generation[index].a + uniform(-0.1, 0.1)
                    generation[i].b = generation[index].b + uniform(-0.1, 0.1)

def calDerCusto(x, y, a, b):
    # utilizando o gradiente descendente 
    # pra achar o valor dos termos da regressão
    somaA = 0
    somaB = 0
    for i in range(len(x)):
        somaA += (x[i]*a + b - y[i])*x[i]
        somaB += (x[i]*a + b - y[i])
        
    return [somaA, somaB]

index = 0

generation = []

for j in range(NUMBER_INDIVIDUALS):
    generation.append(Individual(first_generation=True))

while True:
    cost = []
    
    dadosx = [-2.76, -2.36, -2.40, -2.02, -2, -1.7, -1.64, -1.44, -1.14, -1.17, -1.14, -0.92, -0.54, -0.54, -0.36, -0.132, -0.18, 0.16, 0.28, -2.49, 0.14, 0.65, 0.87, 1.25, 0.85]
    dadosy = [-2.13, -2.01, -1.47, -1.51, -1, -0.41, 0, -0.23, 0.33, 0.65, 1.27, 1.14, 1.23, 1.65, 2.57, 2.73, 2.16, 3.35, 3.05, -2.43, 4.00, 3.93, 4.74, 4.95, 4.38]

    for i in range(NUMBER_INDIVIDUALS):
        plt.plot(dadosx, dadosy, 'o')
        plt.plot([min(dadosx), max(dadosx)], [generation[i].a*min(dadosx)+generation[i].b, generation[i].a*max(dadosx)+generation[i].b])
        cost.append(calDerCusto(dadosx, dadosy, generation[i].a, generation[i].b))
        plt.ylim((-3, 5))
    plt.draw()
    plt.pause(0.1) 
    plt.clf()
    minValue = abs(cost[0][0]) + abs(cost[0][1])
    for k in range(NUMBER_INDIVIDUALS):
        if abs(cost[k][0]) + abs(cost[k][1]) < minValue:
            minValue = abs(cost[k][0]) + abs(cost[k][1])
            index = k

    Individual()