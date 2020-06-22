import math
import random
'''
https://archive.ics.uci.edu/ml/datasets

Aplicação de Machine Learning 
Dataset de pessoas com cancer de mama 
(um grupo de pacientes e um grupo de controle)
Os atributos do conjunto de dados são:
    1- Idade (em anos)
    2- Indice de massa corporea (kg/m2)
    3- Glicose (mg/dL)
    4- Insulina (µU/mL)
    5- HOMA
    6- Leptina (ng/mL)
    7- Adiponectina (µg/mL)
    8- Resistina (ng/mL)
    9- MCP-1 (pg/dL)

O ultimo item (10) diz respeito ao rotulo dos dados (paciente e controle)

'''

def distEuclidiana(dado, teste):
    soma = 0
    for item in range(len(dado)):
        soma += math.pow(dado[item] - teste[item], 2)

    return math.sqrt(soma)

def knn(amostra, comp, k):
    class1, class2 = 0, 0
    while True:
        valor = min(comp)
        classif = comp[valor]
        comp.pop(valor)

        if class1 + class2 <= k:
            if classif == 1:
                class1 += 1
            else:
                class2 += 2
        else:
            if amostra[len(amostra)-1] == 1:
                if class1 > class2:
                    return True
                else:
                    return False
            else:
                if class2 > class1:
                    return True
                else:
                    return False

def votMajor(teste, treino):

    acertos, erros = 0, 0

    for i in range(len(teste)):
        n = {}
        for j in range(len(treino)):
            dist = distEuclidiana(teste[i][:len(teste[i]) - 1], treino[j])
            n.update({dist: treino[j][len(treino[j]) - 1]})

        result = knn(teste[i], n, 15)

        if result:
            acertos += 1
        else:
            erros += 1

    return acertos, erros

# Principal
arquivo = open('C:\\Users\\Sironz\\Desktop\\Relembrando como se programa\\dataset_cancer.txt', 'r')

dataset = []

for linhas in arquivo.readlines():

    linha = linhas.split()
    fora = [8]
    for i in range(len(linha)):
        if linha[i] == '\t' or linha[i] == ' ' or linha[i] == '\n' or i is fora:
            linha.pop(i)
        else:
            linha[i] = int(linha[i])

    dataset.append(linha)

random.shuffle(dataset)

pTreino = 0.7

treino = dataset[:int(len(dataset) * pTreino)]
teste = dataset[int(len(dataset) * pTreino):]

# Treinamento

acertos, erros = votMajor(teste, treino)

print('Porcentagem de acertos: %d' % (100*(acertos / len(teste))))
print('Porcentagem de erros: %d' % (100*(erros / len(teste))))
