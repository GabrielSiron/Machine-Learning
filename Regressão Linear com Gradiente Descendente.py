from random import uniform
from matplotlib import pyplot as plt

def calDerCusto(x, y, a, b):
    # utilizando o gradiente descendente 
    # pra achar o valor dos termos da regressão
    somaA = 0
    somaB = 0
    for i in range(len(x)):
        somaA += (x[i]*a + b - y[i])*x[i]
        somaB += (x[i]*a + b - y[i])
        
    return somaA, somaB

dadosx = [-2.76, -2.36, -2.40, -2.02, -2, -1.7, -1.64, -1.44, -1.14, -1.17, -1.14, -0.92, -0.54, -0.54, -0.36, -0.132, -0.18, 0.16, 0.28, -2.49, 0.14, 0.65, 0.87, 1.25, 0.85]
dadosy = [-2.13, -2.01, -1.47, -1.51, -1, -0.41, 0, -0.23, 0.33, 0.65, 1.27, 1.14, 1.23, 1.65, 2.57, 2.73, 2.16, 3.35, 3.05, -2.43, 4.00, 3.93, 4.74, 4.95, 4.38]

a = uniform(0, 10)
b = uniform(0, 10)

taxaA = 0.01

for i in range(100):
    # atualizando os valores de a e b por gradiente descendente
    somaA, somaB = calDerCusto(dadosx, dadosy, a, b)
    a = a - taxaA*somaA
    b = b - taxaA*somaB
    plt.plot(dadosx, dadosy,'o')
    plt.plot([min(dadosx), max(dadosx)], [a*min(dadosx)+b, a*max(dadosx)+b])
    plt.ylim((-3, 5))
    plt.draw()
    plt.pause(0.001) 
    plt.clf()
    