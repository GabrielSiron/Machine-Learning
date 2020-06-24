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


class Knn:

    def distEuclidiana(self, dado, teste):
        soma = 0
        for item in range(len(dado)):
            soma += math.pow(dado[item] - teste[item], 2)

        return math.sqrt(soma)

    def votMajor(self, rotuloTeste, comp, k):
        class1, class2 = 0, 0
        for i in range(k):
            valor = min(comp)
            rotulo = comp[valor]
            comp.pop(valor)
            print(rotulo, end = '')
            if i != k-1:
                if rotulo == 1:
                    class1 += 1
                else:
                    class2 += 1
            else:
                if rotuloTeste == 1 and class1 > class1:    
                    return True
                elif rotulo Teste == 2 and class2 > class1:
                    return True
                else:
                    return False


    def knn(self, amostra, base):

        n = {}

        for j in range(len(base)):
            dist = self.distEuclidiana(amostra[:len(amostra) - 1], base[j])
            n.update({dist: amostra[len(amostra) - 1]})

        return n

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
testes = dataset[int(len(dataset) * pTreino):]

# Treinamento

classfier = Knn()
acertos, erros = 0, 0

for teste in testes:
    vizinhos = classfier.knn(teste, treino)
    result = classfier.votMajor(teste[-1], vizinhos, 5)
    print(teste[-1])
    if result:
        acertos += 1
    else:
        erros += 1

print('Porcentagem de acertos: %d' % (100*(acertos / len(testes))))
print('Porcentagem de erros: %d' % (100*(erros / len(testes))))
